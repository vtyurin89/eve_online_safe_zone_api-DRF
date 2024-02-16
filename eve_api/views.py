import random
import redis
from rest_framework import permissions
from rest_framework.response import Response
from django.conf import settings
from loguru import logger
from rest_framework.views import APIView

from .serializers import SystemSerializer
from .utils import select_random_object
from .mixins import SystemHandlerMixin
from .base_constants import REDIS_SYSTEM_SETS_KEY


redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

logger.add('logs/main_log.log', format="{time:MMMM D, YYYY > HH:mm:ss} | {level} | {message} | {extra}",
           level="DEBUG", rotation="60 MB", retention="7 days")


class RandomSafeSystemView(APIView, SystemHandlerMixin):
    permission_classes = (permissions.AllowAny,)

    @logger.catch()
    def get(self, request):
        params = request.query_params.get('security_status', 'not_specified')
        logger.info(f"Processing {request.method} request for a random system. Security status: {params}")
        systems_from_redis = redis_client.hget(REDIS_SYSTEM_SETS_KEY, params)

        if not systems_from_redis:
            systems = self._get_systems(params)
            random_system = select_random_object(systems)
            serializer = SystemSerializer(random_system)
            logger.info(f"System taken from database: {random_system.name}")
            return Response(serializer.data, status=200)

        systems_from_redis = eval(systems_from_redis.decode('utf-8'))
        random_system = random.choice(systems_from_redis)
        logger.info(f"System taken from redis cache: {random_system['name']}.")
        return Response(random_system, status=200)



