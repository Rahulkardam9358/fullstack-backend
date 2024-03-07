from django.urls import path, include
from rest_framework.routers import DefaultRouter
from product.views import CategoryViewset, ProductViewset, ReviewViewset


router = DefaultRouter()
router.register('categories', CategoryViewset)
router.register('list', ProductViewset)
router.register('my-reviews', ReviewViewset)


urlpatterns = [
    path('products/', include(router.urls)),
]