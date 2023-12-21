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
        data = requests.get(EVE_SWAGGER_URLS['systems'])
        systems = data.json()
        for index, system in enumerate(systems):
            system = requests.get(EVE_SWAGGER_URLS['systems'] + str(system))
            system = system.json()
            # obj, created = System.objects.get_or_create(
            #     regionid=region['region_id'],
            #     name=region['name'],
            #     description=region['description']
            # )
            # print(f"System {system['system_id']} CREATED")
            print(system)
            if (index + 1) % 30 == 0 and index != 0:
                time.sleep(1)
                print(f"{index + 1} out of {len(systems)}")
        print('DONE')
