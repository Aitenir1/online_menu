from django.urls import path, include
from rest_framework import routers
from cafe.views import DishViewSet, CartViewSet

router = routers.DefaultRouter()
router.register(r'dishes', DishViewSet)
router.register(r'carts', CartViewSet)

urlpatterns = [
    path('api/', include(router.urls))
]