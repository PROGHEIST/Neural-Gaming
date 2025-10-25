from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (UserProfileViewSet, CPUViewSet, GPUViewSet, RAMViewSet,
                    StorageViewSet, MotherboardViewSet, PowerSupplyViewSet)

router = DefaultRouter()
router.register(r'userprofiles', UserProfileViewSet)
router.register(r'cpus', CPUViewSet)
router.register(r'gpus', GPUViewSet)
router.register(r'rams', RAMViewSet)
router.register(r'storages', StorageViewSet)
router.register(r'motherboards', MotherboardViewSet)
router.register(r'powersupplies', PowerSupplyViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
