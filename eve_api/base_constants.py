
# URLS
EVE_SWAGGER_URLS = {
    'systems': "https://esi.evetech.net/dev/universe/systems/",
    'stars': "https://esi.evetech.net/dev/universe/stars/",
    'regions': "https://esi.evetech.net/dev/universe/regions/",
    'constellations': "https://esi.evetech.net/dev/universe/constellations/",
    'stargates': "https://esi.evetech.net/dev/universe/stargates/",
    'stations': "https://esi.evetech.net/dev/universe/stations/",
    'system_kills': "https://esi.evetech.net/dev/universe/system_kills/",
    'system_jumps': "https://esi.evetech.net/dev/universe/system_jumps/"
}


# RESEARCH LIMIT IN HOURS
MAX_HOURS_LIMIT = 168


# Rates - how much each event changes the danger rating
system_action_rates = {
    'ship_jumps': 1,
    'ship_kills': 200,
    'pod_kills': 200,
    'npc_kills': 1,
}
