from django.core.management.base import BaseCommand
import requests
import time


EVE_SWAGGER_URLS = {
    'systems': "https://esi.evetech.net/dev/universe/systems/",
    'stars': "https://esi.evetech.net/dev/universe/stars/",
    'regions': "https://esi.evetech.net/dev/universe/regions/",
    'constellations': "https://esi.evetech.net/dev/universe/constellations/",
    'stargates': "https://esi.evetech.net/dev/universe/stargates/",
    'stations': "https://esi.evetech.net/dev/universe/stargates/",
    'kills': "https://esi.evetech.net/dev/universe/system_kills/",
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = requests.get(EVE_SWAGGER_URLS['kills'])
        kills = data.json()
        filtered_kills = [item for item in kills if item['ship_kills'] == 0 and item['npc_kills'] == 0]
        print(filtered_kills)
        # for index, region in enumerate(regions):
        #     if index % 10 == 0 and index != 0:
        #         print(f"{index} out of {len(regions)}")
        #         time.sleep(1)
        #     region = requests.get(EVE_SWAGGER_URLS['stars'] + str(region))
        #     region = region.json()
        #     print(region)
