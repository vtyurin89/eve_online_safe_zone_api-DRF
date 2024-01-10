import json

from django.http import HttpResponse, JsonResponse
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
import redis

from .models import System
from .serializers import SystemSerializer
from django.conf import settings


redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def system_list(request):
    if request.method == 'GET':
        systems = redis_client.get('system_list')
        if systems is None:
            systems = System.objects.all().prefetch_related('danger_rating_units')
            serializer = SystemSerializer(systems, many=True)
            systems_json = json.dumps(serializer.data)
            redis_client.set('system_list', systems_json)
            return Response(serializer.data, status=200)
        systems = json.loads(systems)
        return Response(systems, status=200)


def system_detail(request, pk):
    try:
        system = System.objects.get(pk=pk)
    except System.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SystemSerializer(system)
        return JsonResponse(serializer.data)
