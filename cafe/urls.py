from django.urls import path, include
from rest_framework import routers
from cafe.views import DishViewSet, CartViewSet, CategoryViewSet, TableViewSet, CartItemViewSet

router = routers.DefaultRouter()
router.register(r'dishes', DishViewSet)
router.register(r'carts', CartViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'tables', TableViewSet)
router.register(r'cart-item', CartItemViewSet)

urlpatterns = [
    path('api/', include(router.urls))
]