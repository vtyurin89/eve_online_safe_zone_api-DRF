from django.core.management.base import BaseCommand
import requests
import time


EVE_SWAGGER_URLS = {
    'systems': "https://esi.evetech.net/dev/universe/systems/",
    'stars': "https://esi.evetech.net/dev/universe/stars/",
    'regions': "https://esi.evetech.net/dev/universe/regions/",
    'constellations': "https://esi.evetech.net/dev/universe/constellations/",
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = requests.get(EVE_SWAGGER_URLS['stars'] + '40000001')
        star = data.json()
        print(star)
        # for index, region in enumerate(regions):
        #     if index % 10 == 0 and index != 0:
        #         print(f"{index} out of {len(regions)}")
        #         time.sleep(1)
        #     region = requests.get(EVE_SWAGGER_URLS['stars'] + str(region))
        #     region = region.json()
        #     print(region)
        print('DONE')