from eve.celery import app
import requests
import json
import redis

from .models import System, DangerRating
from .base_constants import EVE_SWAGGER_URLS, system_action_rates
from .serializers import SystemSerializer


@app.task
def update_star_db():
    def convert_kills_to_dict(d: dict):
        # we multiply the number of events by the corresponding rating,
        # then sum everything to make overall danger rating of the system for the hour (based on kills)
        system_id = d.pop('system_id')
        return sum([system_action_rates.get(key, 0) * value for key, value in d.items() if value > 0])

    def convert_jumps_to_dict(d: dict):
        # we multiply the number of jumps by the corresponding rating,
        # this is the danger rating of the system for the hour (based on system jumps)
        system_id = d.pop('system_id')
        return system_action_rates.get('ship_jumps') * d.get('ship_jumps')

    system_kills = requests.get(EVE_SWAGGER_URLS['system_kills']).json()
    system_kills_dict = {item['system_id']: convert_kills_to_dict(item) for item in system_kills}

    system_jumps = requests.get(EVE_SWAGGER_URLS['system_jumps']).json()
    system_jumps_dict = {item['system_id']: convert_jumps_to_dict(item) for item in system_jumps}

    #time to calculate danger rating of the systems
    system_rating_change = {key: system_kills_dict.get(key, 0) + system_jumps_dict.get(key, 0)
                            for key in set(system_kills_dict.keys()).union(set(system_jumps_dict.keys()))}

    #adding safe systems (eve api does not return them)
    missing_systems = System.objects.exclude(system_id__in=system_rating_change)
    safe_systems_rating_change = {system.system_id: 0 for system in missing_systems}
    system_rating_change.update(safe_systems_rating_change)

    #creating new rating objects
    danger_rating_instances = [DangerRating(
            system_id=key,
            value=system_rating_change[key],
        )
        for key in system_rating_change]
    DangerRating.objects.bulk_create(danger_rating_instances)

    systems = System.objects.all().prefetch_related('danger_rating_units')
    serializer = SystemSerializer(systems, many=True)
    systems_json = json.dumps(serializer.data)
    my_redis = redis.StrictRedis(host='localhost', port=6379, db=0)
    my_redis.set('latest_rating', systems_json)

