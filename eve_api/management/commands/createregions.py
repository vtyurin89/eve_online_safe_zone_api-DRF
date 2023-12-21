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
        data = requests.get(EVE_SWAGGER_URLS['regions'])
        regions = data.json()
        for index, region in enumerate(regions):
            region = requests.get(EVE_SWAGGER_URLS['regions'] + str(region))
            region = region.json()
            obj, created = Region.objects.get_or_create(
                regionid=region['region_id'],
                name=region['name'],
                description=region['description']
            )
            if created:
                print(f"Region {region['region_id']} CREATED")
            else:
                print(f"Region {region['region_id']} ALREADY EXISTS")
            if (index + 1) % 30 == 0 and index != 0:
                time.sleep(1)
                print(f"{index + 1} out of {len(regions)}")
        print('DONE')