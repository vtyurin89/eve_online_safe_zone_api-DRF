import json
import requests
import redis
from django.db.models import QuerySet
from django.conf import settings
from eve.celery import app
from typing import Dict, Union
from django.utils import timezone
from datetime import timedelta
from loguru import logger

from .mixins import SystemHandlerMixin
from .models import System, DangerRating
from .serializers import SystemSerializer
from .base_constants import EVE_SWAGGER_URLS, system_event_rates, \
    MAX_HOURS_LIMIT, SYSTEM_SECURITY_LEVELS, REDIS_SYSTEM_SETS_KEY, REDIS_KEY_DELETE_IN_SECONDS


logger.remove()
logger.add('logs/main_log.log', format="{time:MMMM D, YYYY > HH:mm:ss} | {level} | {message} | {extra}",
           level="DEBUG", rotation="60 MB", retention="7 days")


redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


class UpdateStarDb(SystemHandlerMixin):
    logger = logger
    """
    This class updates database every hour, creating a DangerRating object for every System object.
    """
    def __init__(self):
        self.DEFAULT_SYSTEM_VALUES = {
            'npc_kills': 0,
            'pod_kills': 0,
            'ship_kills': 0,
            'ship_jumps': 0,
        }
        self.system_data: Dict[int, Dict[str, Union[int, float]]] = {}

    def _process_system_kills(self) -> None:

        system_kills = requests.get(EVE_SWAGGER_URLS['system_kills']).json()
        with open('recent_data/5-kills_json.txt', 'w') as f:
            json.dump(system_kills, f)

        for item in system_kills:
            self.system_data.setdefault(item['system_id'], {}).update({
                'npc_kills': item['npc_kills'],
                'pod_kills': item['pod_kills'],
                'ship_kills': item['ship_kills'],
            })
        with open('recent_data/1-system_kills.txt', 'w') as f:
            json.dump(self.system_data, f)

    def _process_system_jumps(self) -> None:

        # Star system IDs in here may be different from IDs we got in the method above.
        # We need to update the system_data dictionary with missing IDs.
        system_jumps = requests.get(EVE_SWAGGER_URLS['system_jumps']).json()
        with open('recent_data/6-jumps_json.txt', 'w') as f:
            json.dump(system_jumps, f)
        for item in system_jumps:
            system_id = item['system_id']
            self.system_data.setdefault(system_id, {}).update({'ship_jumps': item['ship_jumps']})
        with open('recent_data/2-system_kills-jumps.txt', 'w') as f:
            json.dump(self.system_data, f)

    def _process_missing_systems(self) -> None:

        # Eve Swagger API only returns info about systems where kills and ship jumps happened.
        # Now we need to add systems where no kills and no ship jumps happened.

        missing_systems = System.objects.exclude(system_id__in=self.system_data)
        safe_systems_dict = {system.system_id: self.DEFAULT_SYSTEM_VALUES for system in missing_systems}
        self.system_data.update(safe_systems_dict)
        with open('recent_data/3-system_kills-jumps-missimg.txt', 'w') as f:
            json.dump(self.system_data, f)

    def _calculate_rating(self) -> None:
        for item in self.system_data:
            self.system_data[item]['rating_change'] = sum([
                system_event_rates.get(key, 0) * value
                for key, value in self.system_data[item].items()
            ])
        with open('recent_data/4-system_kills-jumps-missimg-rating.txt', 'w') as f:
            json.dump(self.system_data, f)

    def _create_new_rating_objects(self) -> None:
        danger_rating_instances = [
            DangerRating(system_id=key, value=self.system_data[key]['rating_change'])
            for key in self.system_data
        ]
        DangerRating.objects.bulk_create(danger_rating_instances)
        self.logger.info(f"DB update by celery -- {len(danger_rating_instances)} new 'DangerRating' objects created.")

    def _update_redis_sets(self, redis_key: str, redis_expiration_in_seconds: int) -> None:
        security_levels = [key for key in SYSTEM_SECURITY_LEVELS] + ['not_specified']
        pipeline = redis_client.pipeline()

        for security_status_key in security_levels:
            systems = self._get_systems(security_status_key)
            serialized_systems = SystemSerializer(systems, many=True).data
            serialized_systems_json = json.dumps(serialized_systems)
            pipeline.hset(redis_key, security_status_key, serialized_systems_json)
            self.logger.info(f"Redis update {redis_key}: {security_status_key} with {systems.count()} systems:\
                                        {[system_dict['name'] for system_dict in serialized_systems]}")

        pipeline.execute()
        redis_client.expire(redis_key, redis_expiration_in_seconds)

    @logger.catch
    def execute(self) -> None:
        self._process_system_kills()
        self._process_system_jumps()
        self._process_missing_systems()
        self._calculate_rating()
        self._create_new_rating_objects()
        self._update_redis_sets(REDIS_SYSTEM_SETS_KEY, REDIS_KEY_DELETE_IN_SECONDS)


class DeleteOldRates:
    logger = logger
    """
    This class deletes old DangerRating objects.
    The frequency of this action depends on the max_hours_limit variable,
    it determines the number of HOURS (converted to DAYS) that the DangerRating objects remain relevant.
    """
    def __init__(self, max_hours_limit: int):
        self.days_range = max_hours_limit // 24
        time_now = timezone.localtime(timezone.now())
        self.time_starting_point = time_now - timedelta(days=self.days_range)
        self.logger.info(f"DB update by celery -- 'DangerRating' objects created before {self.time_starting_point} will be deleted!")

    def _get_outdated_danger_rating_objects(self) -> QuerySet[DangerRating]:
        outdated_objects = DangerRating.objects.exclude(
            timestamp__range=(self.time_starting_point, timezone.now())
        )
        return outdated_objects

    @logger.catch
    def execute(self) -> None:
        outdated_objects = self._get_outdated_danger_rating_objects()
        outdated_objects_count = outdated_objects.count()
        outdated_objects.delete()
        self.logger.info(f"DB update by celery -- {outdated_objects_count} outdated 'DangerRating' objects successfully deleted.")


@app.task
def update_star_db_task():
    update_star_db = UpdateStarDb()
    update_star_db.execute()


@app.task
def delete_outdated_rates_task():
    delete_old_rates = DeleteOldRates(MAX_HOURS_LIMIT)
    delete_old_rates.execute()
