from django.shortcuts import render
from rest_framework import viewsets

from cafe.models import Dish, Cart, Category
from cafe.serializers import DishSerializer, CartSerializer, CategorySerializer


class DishViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

