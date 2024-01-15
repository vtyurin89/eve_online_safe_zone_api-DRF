from django.core.management.base import BaseCommand
import requests
import time

from ...models import Constellation, Region

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
            constellation = requests.get(EVE_SWAGGER_URLS['constellations'] + str(constellation))
            constellation = constellation.json()
            obj, created = Constellation.objects.get_or_create(
                constellation=constellation['constellation_id'],
                name=constellation['name'],
                x=constellation['position']['x'],
                y=constellation['position']['y'],
                z=constellation['position']['z'],
                region=Region.objects.get(regionid=constellation['region_id']),
            )
            if created:
                print(f"Constellation {constellation['constellation_id']} CREATED")
            else:
                print(f"Constellation {constellation['constellation_id']} ALREADY EXISTS")
            if (index + 1) % 30 == 0 and index != 0:
                print(f"{index} out of {len(constellations)}")
                time.sleep(1)
        print('DONE')
