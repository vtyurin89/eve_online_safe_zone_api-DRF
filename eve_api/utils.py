from django.db.models import Count
import random

from .base_constants import SYSTEM_SECURITY_LEVELS


def get_filter_kwargs(value: str):
    """
    The API allows urls like /?security_status=high-sec or /?security_status=low-sec
    :param value:  one of the keys in SYSTEM_SECURITY_LEVELS
    :return: dictionary to be used in a filter
    """
    if value not in SYSTEM_SECURITY_LEVELS:
        return {}
    filter_kwargs = {
        'security_status__gte': SYSTEM_SECURITY_LEVELS[value][0],
        'security_status__lte': SYSTEM_SECURITY_LEVELS[value][1],
    }
    return filter_kwargs


def select_random_object(input_queryset):
    """
    :param input_queryset: queryset
    :return: random object from the queryset
    """

    queryset_count = input_queryset.aggregate(count=Count('pk'))['count']
    random_index = random.randint(0, queryset_count - 1)
    return input_queryset[random_index]


