from django.core.management.base import BaseCommand
import redis




class Command(BaseCommand):
    def handle(self, *args, **options):

        my_redis = redis.Redis(host='localhost', port=6379, db=0)