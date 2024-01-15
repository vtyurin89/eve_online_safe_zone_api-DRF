import json
import redis
from django.db.models import Sum, OuterRef, Count, Subquery, Q
from django.http import HttpResponse, JsonResponse
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

from .models import System, DangerRating
from .serializers import SystemSerializer
from .utils import get_filter_kwargs, select_random_object
from .base_constants import QUERY_RESULT_CUT_SIZE, MAX_HOURS_LIMIT


redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


# cashing not implemented yet

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_random_safe_system(request):
    if request.method == 'GET':
        params = request.query_params
        # systems_redis = redis_client.get('system_list')

        filter_kwargs = get_filter_kwargs(params.get('security_status', ''))

        days_range = MAX_HOURS_LIMIT // 24
        time_starting_point = timezone.now() - timedelta(days=days_range)

        systems_redis = None
        if systems_redis is None:

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

            random_system = select_random_object(systems)

            serializer = SystemSerializer(random_system)
            return Response(serializer.data, status=200)
        systems = json.loads(systems_redis)
        return Response(systems, status=200)


def system_detail(request, pk):
    try:
        system = System.objects.get(pk=pk)
    except System.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SystemSerializer(system)
        return JsonResponse(serializer.data)
