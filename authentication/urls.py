from django.urls import path, include
from rest_framework.routers import DefaultRouter
from authentication.views import AddressViewset
from order.views import OrderViewset


router = DefaultRouter()
router.register('address', AddressViewset)
router.register('orders', OrderViewset)


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('rest_framework.urls')),
    path('auth/users/', include(router.urls)),
]