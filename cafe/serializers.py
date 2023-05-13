from rest_framework import serializers
from cafe.models import Dish, Cart, Category


class CartSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'dishes']
        extra_kwargs = {'dishes': {'required': False}}


class DishSerializer(serializers.HyperlinkedModelSerializer):
    carts = CartSerializer(many=True, read_only=True)

    class Meta:
        model = Dish
        fields = ['id', 'name_en', 'name_kg', 'name_ru', 'description_en', 'description_kg', 'description_ru', 'price',
                  'gram', 'category', 'image', 'carts']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

