from rest_framework import serializers
from cafe.models import Dish, Category, Table, Order, OrderItem


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TableSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'url']


class DishSerializer(serializers.HyperlinkedModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Dish
        fields = ['id', 'name_en', 'name_kg', 'name_ru',
                  'description_en', 'description_kg', 'description_ru',
                  'price', 'gram', 'category_name', 'image']

    @staticmethod
    def get_category_name(obj):
        return obj.category.name


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['dish', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    time_created = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = Order
        fields = ['id', 'table', 'time_created', 'status', 'payment', 'is_takeaway', 'total_price', 'items']

    def create(self, validated_data: dict):
        order_items = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        total_sum = 0
        for order_item in order_items:
            dish = order_item['dish']
            quantity = order_item['quantity']

            OrderItem.objects.create(
                dish=dish,
                order=order,
                quantity=quantity
            )

            total_sum += dish.price * quantity

        order.total_price = total_sum
        order.save()

        return order
