import json

from django.http import HttpResponse, JsonResponse
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import redis

from .models import System
from .serializers import SystemSerializer

from django.db import connection


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def system_list(request):
    if request.method == 'GET':
        my_redis = redis.Redis(host='localhost', port=6379, db=0)
        result = json.loads(my_redis.get('latest_rating').decode('utf-8'))
        return Response(result)


def system_detail(request, pk):
    try:
        system = System.objects.get(pk=pk)
    except System.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SystemSerializer(system)
        return JsonResponse(serializer.data)
