from django.urls import path, include
from rest_framework import routers
from cafe.views import DishViewSet, CartViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register(r'dishes', DishViewSet)
router.register(r'carts', CartViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('api/', include(router.urls))
]