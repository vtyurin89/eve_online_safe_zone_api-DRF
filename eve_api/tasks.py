from eve.celery import app
import requests
from typing import Dict, List, Union

from .models import System, DangerRating
from .base_constants import EVE_SWAGGER_URLS, system_event_rates


class UpdateStarDb:
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
        for item in system_kills:
            self.system_data.setdefault(item['system_id'], {}).update({
                'npc_kills': item['npc_kills'],
                'pod_kills': item['pod_kills'],
                'ship_kills': item['ship_kills'],
            })

    def _process_system_jumps(self) -> None:

        # Star system IDs in here may be different from IDs we got in the method above.
        # We need to update the system_data dictionary with missing IDs.
        system_jumps = requests.get(EVE_SWAGGER_URLS['system_jumps']).json()
        for item in system_jumps:
            system_id = item['system_id']
            self.system_data.setdefault(system_id, {}).update({'ship_jumps': item['ship_jumps']})

    def _process_missing_systems(self) -> None:

        # Eve Swagger API only returns info about systems where kills and ship jumps happened.
        # Now we need to add systems where no kills and no ship jumps happened.

        missing_systems = System.objects.exclude(system_id__in=self.system_data)
        safe_systems_dict = {system.system_id: self.DEFAULT_SYSTEM_VALUES for system in missing_systems}
        self.system_data.update(safe_systems_dict)

    def _calculate_rating(self) -> None:
        for item in self.system_data:
            self.system_data[item]['rating_change'] = sum([
                system_event_rates.get(key, 0) * value
                for key, value in self.system_data[item].items()
            ])

    def _create_new_rating_objects(self) -> None:
        danger_rating_instances = [
            DangerRating(system_id=key, value=self.system_data[key]['rating_change'])
            for key in self.system_data
        ]
        DangerRating.objects.bulk_create(danger_rating_instances)

    def execute(self) -> None:
        self._process_system_kills()
        self._process_system_jumps()
        self._process_missing_systems()
        self._calculate_rating()
        self._create_new_rating_objects()


@app.task
def update_star_db_task():
    update_star_db = UpdateStarDb()
    update_star_db.execute()


# old code to be deleted...
# @app.task
# def update_star_db():
#
#     system_kills = requests.get(EVE_SWAGGER_URLS['system_kills']).json()
#     system_jumps = requests.get(EVE_SWAGGER_URLS['system_jumps']).json()
#     system_dict = {item['system_id']:
#         {
#             'npc_kills': item['npc_kills'],
#             'pod_kills': item['pod_kills'],
#             'ship_kills': item['ship_kills']
#         }
#         for item in system_kills}
#
#     for item in system_jumps:
#         if item['system_id'] not in system_dict:
#             system_dict[item['system_id']] = {
#                 'npc_kills': 0,
#                 'pod_kills': 0,
#                 'ship_kills': 0,
#                 'ship_jumps': item['ship_jumps'],
#             }
#         else:
#             system_dict[item['system_id']].update({'ship_jumps': item['ship_jumps']})
#
#     missing_systems = System.objects.exclude(system_id__in=system_dict)
#     safe_systems_dict = {system.system_id:
#         {
#             'npc_kills': 0,
#             'pod_kills': 0,
#             'ship_kills': 0,
#             'ship_jumps': 0,
#         }
#         for system in missing_systems}
#     system_dict.update(safe_systems_dict)
#     for item in system_dict:
#         system_dict[item]['rating_change'] = sum([system_event_rates.get(key, 0) * value
#                                                   for key, value in system_dict[item].items()])
#     # with open("eve_api/eve_log.txt", "a") as log_file:
#     #     log_file.write(f'============NEW RECORDING: {time.ctime()} =============\n')
#     #     log_file.write(f"{system_dict}\n")
#
#     #creating new rating objects
#     danger_rating_instances = [DangerRating(
#             system_id=key,
#             value=system_dict[key]['rating_change'],
#         )
#         for key in system_dict]
#     DangerRating.objects.bulk_create(danger_rating_instances)
#
