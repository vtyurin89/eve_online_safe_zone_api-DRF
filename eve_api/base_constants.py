
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
# Select numbers which are divisible by 24
MAX_HOURS_LIMIT = 168

# Number of systems which will be in a 'safe' sample
QUERY_RESULT_CUT_SIZE = 30


# Standard security rates of star systems
SYSTEM_SECURITY_LEVELS = {
    'high-sec': (0.45, 1),
    'low-sec': (0.045, 0.44999999999999),
    'null-sec': (-0.94999999999999, 0.044999999999999),
    'wormhole': (-1, -0.95),
}


# Rates - how much each event changes the danger rating
system_event_rates = {
    'ship_jumps': 1,
    'ship_kills': 200,
    'pod_kills': 200,
    'npc_kills': 1,
}
