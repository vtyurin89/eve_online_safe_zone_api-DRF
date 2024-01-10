import json

from django.http import HttpResponse, JsonResponse
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import redis

from .models import System
from .serializers import SystemSerializer
from django.conf import settings

from django.db import connection


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def system_list(request):
    if request.method == 'GET':
        my_redis = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
        result = json.loads(my_redis.get('latest_rating').decode('utf-8'))
        return Response(result, status=200)


def system_detail(request, pk):
    try:
        system = System.objects.get(pk=pk)
    except System.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SystemSerializer(system)
        return JsonResponse(serializer.data)
