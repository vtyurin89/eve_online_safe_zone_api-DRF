from eve.celery import app
import requests
import json
import redis
import time
from django.conf import settings

from .models import System, DangerRating
from .serializers import SystemSerializer
from .base_constants import EVE_SWAGGER_URLS, system_event_rates


@app.task
def update_star_db():

    system_kills = requests.get(EVE_SWAGGER_URLS['system_kills']).json()
    system_jumps = requests.get(EVE_SWAGGER_URLS['system_jumps']).json()
    system_dict = {item['system_id']:
        {
            'npc_kills': item['npc_kills'],
            'pod_kills': item['pod_kills'],
            'ship_kills': item['ship_kills']
        }
        for item in system_kills}

    for item in system_jumps:
        if item['system_id'] not in system_dict:
            system_dict[item['system_id']] = {
                'npc_kills': 0,
                'pod_kills': 0,
                'ship_kills': 0,
                'ship_jumps': item['ship_jumps'],
            }
        else:
            system_dict[item['system_id']].update({'ship_jumps': item['ship_jumps']})
    missing_systems = System.objects.exclude(system_id__in=system_dict)
    safe_systems_dict = {system.system_id:
        {
            'npc_kills': 0,
            'pod_kills': 0,
            'ship_kills': 0,
            'ship_jumps': 0,
        }
        for system in missing_systems}
    system_dict.update(safe_systems_dict)
    for item in system_dict:
        system_dict[item]['rating_change'] = sum([system_event_rates.get(key, 0) * value
                                                  for key, value in system_dict[item].items()])
    with open("eve_api/eve_log.txt", "a") as log_file:
        log_file.write(f'============NEW RECORDING: {time.ctime()} =============\n')
        log_file.write(f"{system_dict}\n")

    #creating new rating objects
    danger_rating_instances = [DangerRating(
            system_id=key,
            value=system_dict[key]['rating_change'],
        )
        for key in system_dict]
    DangerRating.objects.bulk_create(danger_rating_instances)


    #update systems in redis
    systems = System.objects.all().prefetch_related('danger_rating_units')
    serializer = SystemSerializer(systems, many=True)
    systems_json = json.dumps(serializer.data)
    my_redis = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
    my_redis.set('system_list', systems_json)

