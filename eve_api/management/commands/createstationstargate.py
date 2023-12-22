from django.core.management.base import BaseCommand
import requests
import time

from ...models import Station, System, Stargate

EVE_SWAGGER_URLS = {
    'systems': "https://esi.evetech.net/dev/universe/systems/",
    'stars': "https://esi.evetech.net/dev/universe/stars/",
    'regions': "https://esi.evetech.net/dev/universe/regions/",
    'constellations': "https://esi.evetech.net/dev/universe/constellations/",
    'stargates': "https://esi.evetech.net/dev/universe/stargates/",
    'stations': "https://esi.evetech.net/dev/universe/stations/",
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        data = requests.get(EVE_SWAGGER_URLS['systems'])
        systems = data.json()

        timeout_counter = 0

        for index, system in enumerate(systems):
            system = requests.get(EVE_SWAGGER_URLS['systems'] + str(system))
            system = system.json()
            stargates = system.get('stargates')
            stations = system.get('stations')

            if stations:
                for station in stations:
                    station = requests.get(EVE_SWAGGER_URLS['stations'] + str(station))
                    station = station.json()

                    obj, created = Station.objects.get_or_create(
                        station_id=station['station_id'],
                        name=station['name'],
                        x=station['position']['x'],
                        y=station['position']['y'],
                        z=station['position']['z'],
                        system=System.objects.get(system_id=station['system_id'])
                    )
                    if created:
                        print(f"Station {station['station_id']} CREATED")
                    else:
                        print(f"Station {station['station_id']} ALREADY EXISTS")

                    timeout_counter += 1
                    if timeout_counter % 30 == 0 and index != 0:
                        time.sleep(1)

            if stargates:
                for stargate in stargates:
                    stargate = requests.get(EVE_SWAGGER_URLS['stargates'] + str(stargate))
                    stargate = stargate.json()

                    obj, created = Stargate.objects.get_or_create(
                        stargate_id=stargate['stargate_id'],
                        name=stargate['name'],
                        x=stargate['position']['x'],
                        y=stargate['position']['y'],
                        z=stargate['position']['z'],
                        system=System.objects.get(system_id=stargate['system_id'])
                    )
                    if created:
                        print(f"Stargate {stargate['stargate_id']} CREATED")
                    else:
                        print(f"Stargate {stargate['stargate_id']} ALREADY EXISTS")

                    timeout_counter += 1
                    if timeout_counter % 30 == 0 and index != 0:
                        time.sleep(1)

            timeout_counter += 1
            if timeout_counter % 30 == 0 and index != 0:
                time.sleep(1)

            if (index + 1) % 30 == 0 and index != 0:
                print(f"{index + 1} out of {len(systems)}")

        print('DONE')

