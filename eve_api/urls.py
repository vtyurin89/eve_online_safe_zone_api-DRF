from django.urls import path

from .views import *

urlpatterns = [
    path('api/v1/systems/', system_list),
    path('api/v1/systems/<int:pk>/', system_detail),
]