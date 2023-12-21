from django.core.management.base import BaseCommand
import requests
import time

from ...models import Region

EVE_SWAGGER_URLS = {
    'systems': "https://esi.evetech.net/dev/universe/systems/",
    'stars': "https://esi.evetech.net/dev/universe/stars/",
    'regions': "https://esi.evetech.net/dev/universe/regions/",
    'constellations': "https://esi.evetech.net/dev/universe/constellations/",
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = requests.get(EVE_SWAGGER_URLS['constellations'])
        constellations = data.json()
        for index, constellation in enumerate(constellations):
            if index % 10 == 0 and index != 0:
                time.sleep(1)
            constellation = requests.get(EVE_SWAGGER_URLS['constellations'] + str(constellation))
            constellation = constellation.json()
            # Region.objects.create(
            #     regionid=region['region_id'],
            #     name=region['name'],
            #     description=region['description']
            # )
            print(constellation)
        print('DONE')
