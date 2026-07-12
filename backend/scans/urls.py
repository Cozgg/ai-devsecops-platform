from django.urls import include, path
from rest_framework.routers import DefaultRouter

from scans.views import ScanJobViewSet

router = DefaultRouter()
router.register("", ScanJobViewSet, basename="scan")

urlpatterns = [
    path("", include(router.urls)),
]
