from django.core.management.base import BaseCommand
import requests
import time

from ...models import System

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
            obj, created = System.objects.get_or_create(
                system_id=system['system_id'],
                constellation_id=system['constellation_id'],
                name=system['name'],
                x=system['position']['x'],
                y=system['position']['y'],
                z=system['position']['z'],
                security_status=system['security_status'],
                security_class=system.get('security_class', ''),
            )
            if created:
                print(f"System {system['system_id']} CREATED")
            else:
                print(f"System {system['system_id']} ALREADY EXISTS")
            if (index + 1) % 30 == 0 and index != 0:
                time.sleep(1)
                print(f"{index + 1} out of {len(systems)}")
        print('DONE')
