from django.http import HttpResponse, JsonResponse

from .models import System
from .serializers import SystemSerializer


def system_list(request):
    if request.method == 'GET':
        systems = System.objects.all()
        serializer = SystemSerializer(systems, many=True)
        return JsonResponse(serializer.data, safe=False)


def system_detail(request, pk):
    try:
        system = System.objects.get(pk=pk)
    except System.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SystemSerializer(system)
        return JsonResponse(serializer.data)
