import redis
from django.db.models import Sum, OuterRef, Subquery
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from loguru import logger

from .models import System, DangerRating
from .serializers import SystemSerializer
from .utils import get_filter_kwargs, select_random_object
from .base_constants import QUERY_RESULT_CUT_SIZE, MAX_HOURS_LIMIT


redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

logger.add('logs/main_logs/main_log.log', format="{time:MMMM D, YYYY > HH:mm:ss} | {level} | {message} | {extra}",
           level="DEBUG", rotation="50 MB")


# cashing not implemented yet

@logger.catch
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_random_safe_system(request):
    # The function returns a random safe system based on the request and its parameters.
    # The request may have a parameter 'security_status' (high-sec, low-sec, null-sec or wormhole).
    # Constants MAX_HOURS_LIMIT and QUERY_RESULT_CUT_SIZE can be adjusted in base_constants.py

    if request.method == 'GET':
        # logger.info("==== STARTING NEW REQUEST LOG ====")

        params = request.query_params
        # systems_redis = redis_client.get('system_list')

        filter_kwargs = get_filter_kwargs(params.get('security_status', ''))

        # Checking time period
        days_range = MAX_HOURS_LIMIT // 24
        time_now = timezone.localtime(timezone.now())
        time_starting_point = time_now - timedelta(days=days_range)
        # logger.info(f"Checking time period: between {time_starting_point} and {time_now}")

        systems = System.objects.filter(**filter_kwargs).annotate(
            danger_rating=Subquery(
                DangerRating.objects.filter(
                    system=OuterRef('pk'),
                    timestamp__range=(time_starting_point, timezone.now())
                )
                .values('system')
                .annotate(rate_sum=Sum('value'))
                .values('rate_sum')[:1]
            )
        ).order_by('danger_rating')[:QUERY_RESULT_CUT_SIZE]

        # Logging for debugging
        # system_logger = logger.bind(systems=systems)
        random_system = select_random_object(systems)
        # system_logger.bind(random_system=random_system).debug(f"Random system selected: {random_system}")

        serializer = SystemSerializer(random_system)
        return Response(serializer.data, status=200)

