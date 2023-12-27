from eve.celery import app
from .base_constants import EVE_SWAGGER_URLS, system_action_rates, MAX_RATE_CHANGE
import requests


@app.task
def update_star_db():
    def convert_dict_to_rating(d: dict):
        d.pop('system_id')
        # return min(sum([system_action_rates.get(key, 0) for key, value in d.items() if value > 0]), MAX_RATE_CHANGE)
        return [system_action_rates[key] for key, value in d.items() if value > 0]

    system_kills = requests.get(EVE_SWAGGER_URLS['system_kills']).json()
    danger_level_change = {item['system_id']: convert_dict_to_rating(item) for item in system_kills }

    # system_jumps = requests.get(EVE_SWAGGER_URLS['system_jumps']).json()
    # for item in system_jumps:
    #     system_jumps_rating = system_action_rates['ship_jumps'] if item['ship_jumps'] > 0 else 0
    #     danger_level_change[item['system_id']] = min(danger_level_change[item['system_id']] + system_jumps_rating, MAX_RATE_CHANGE)

    with open('eve_api/eve_log.txt', 'a', encoding='utf-8') as log_file:
        log_file.write(f"{danger_level_change}\n")
        log_file.write(f"{system_kills}\n")

