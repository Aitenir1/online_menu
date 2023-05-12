from rest_framework import serializers
from cafe.models import Dish, Cart

class DishSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dish
        fields = '__all__'


class CartSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

