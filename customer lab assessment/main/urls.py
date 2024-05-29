from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, DestinationViewSet, handle_incoming_data

router = DefaultRouter()
router.register('accounts', AccountViewSet)
router.register('destinations', DestinationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('server/incoming_data', handle_incoming_data),
]
