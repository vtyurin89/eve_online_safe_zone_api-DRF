from django.core.management.base import BaseCommand
import redis
import json
from ...models import System, DangerRating
from ...serializers import SystemSerializer


class Command(BaseCommand):
    def handle(self, *args, **options):

        my_redis = redis.Redis(host='localhost', port=6379, db=0)