from django.urls import path
from .views import ListPublicPool

urlpatterns = [
    path("", ListPublicPool.as_view(), name="pool.public.list")
]
