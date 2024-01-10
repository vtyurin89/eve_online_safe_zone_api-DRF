from django.core.management.base import BaseCommand
import requests
import time

from ...base_constants import EVE_SWAGGER_URLS, system_action_rates
from ...models import System


class Command(BaseCommand):
    def handle(self, *args, **options):
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
            system_dict[item]['rating_change'] = sum([system_action_rates.get(key, 0) * value
                                                      for key, value in system_dict[item].items()])
        with open("eve_api/eve_log.txt", "a") as log_file:
            log_file.write(f'============NEW RECORDING: {time.ctime()} =============\n')
            log_file.write(f"{system_dict}\n")