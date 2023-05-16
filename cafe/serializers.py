from rest_framework import serializers
from cafe.models import Dish, Cart, Category, Table, CartItem


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'url']


class DishSerializer(serializers.HyperlinkedModelSerializer):
    # carts = CartSerializer(many=True, read_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Dish
        fields = ['id', 'name_en', 'name_kg', 'name_ru', 'description_en', 'description_kg', 'description_ru', 'price',
                  'gram', 'category', 'image']


class CartItemSerializer(serializers.ModelSerializer):
    # dish = DishSerializer(many=True)

    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    # dishes = DishSerializer(many=True, read_only=True)
    # dishes = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all(), many=True)
    # table = serializers.PrimaryKeyRelatedField(queryset=Table.objects.all(), read_only=False)
    # items = CartItemSerializer(many=True)

    def to_representation(self, instance):
        # self.fields['table_id'] = serializers.PrimaryKeyRelatedField(queryset=Dish.objects.all())
        # self.fields['table_id'] =

        return super(CartSerializer, self).to_representation(instance)

    def get_items(self, obj):
        dishes = Dish.objects.filter(cartitem__cart=self)
        serializer = DishSerializer(dishes, many=True)
        return serializer.data

    # def create(self, validated_date):
    #     table = validated_date.pop('table')
    #     cart = Cart.objects.create(**validated_date)
    #
    #     # table.objects
    #
    #     return cart

    class Meta:
        model = Cart
        # fields = ['id', 'dishes']
        fields = ['id', 'table']
        # extra_kwargs = {'dishes': {'required': False}}