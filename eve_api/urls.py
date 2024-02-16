from django.urls import path

from .views import *

urlpatterns = [
    path('api/v1/safe_systems/random/', RandomSafeSystemView.as_view()),
]