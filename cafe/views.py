from django.shortcuts import render
from rest_framework import viewsets

from cafe.models import Dish, Cart
from cafe.serializers import DishSerializer, CartSerializer

class DishViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer

class CartViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
