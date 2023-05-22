from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action

from cafe.models import Dish, Category, Table, Order, OrderItem
from cafe.serializers import DishSerializer, OrderSerializer

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect

class DishViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class OrderViewSet(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy('home')


class OrderListView(ListView):
    model = Order
    template_name = 'orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = super().get_queryset()

        return queryset.filter(status=0)


def complete_order(request, pk):
    if request.method == 'POST':
        order = Order.objects.get(id=pk)
        order.status = 1
        order.generate_cheque()
        order.save()
        return redirect('home')

    return render(request, 'complete_order.html')

# class CartViewSet(viewsets.ModelViewSet):
#     # lookup_field = 'ip_address'
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer
#
#     def create(self, request, *args, **kwargs):
#         table = request.data.get('table')
#
#         try:
#             eo = Cart.objects.get(table=table)
#
#             seconds_passed = (timezone.now() - eo.created_at).total_seconds()
#             print(f"Created {seconds_passed} seconds ago")
#             if seconds_passed > 400:
#                 eo.delete()
#                 raise Cart.DoesNotExist
#             serializer = self.get_serializer(eo)
#
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Cart.DoesNotExist:
#             pass
#
#         return super().create(request, *args, **kwargs)
#
#     @action(detail=True, methods=['post'])
#     def add_to_cart(self, request, pk=None):
#         cart = self.get_object()
#         food_id = request.data.get('dish')
#         quantity = request.data.get('quantity')
#         try:
#             cart_item = CartItem.objects.get(cart=cart, dish=food_id)
#             cart_item.quantity += quantity
#             cart_item.save()
#         except CartItem.DoesNotExist:
#             cart_item = CartItem.objects.create(cart=cart, dish=Dish.objects.get(id=food_id), quantity=quantity)
#         serializer = CartItemSerializer(cart_item)
#         return Response(CartSerializer(cart).data)
#
#     @action(detail=True, methods=['post'])
#     def remove_from_cart(self, request, pk=None):
#         print(pk)
#
#         cart = self.get_object()
#         dish_id = request.data.get('dish')
#
#         cart_item = CartItem.objects.filter(cart=cart, dish=Dish.objects.get(id=dish_id)).first()
#
#         if cart_item:
#             cart_item.delete()
#
#         return Response({'message': 'Food removed from cart'})
#
#     @action(detail=True, methods=['post'])
#     def checkout(self, request, pk=None):
#         cart = self.get_object()
#         payment = request.data.get('payment')
#         is_takeaway = request.data.get('is_takeaway')
#         cart_items = CartItem.objects.filter(cart=cart)
#         order = Order.objects.create(table=cart.table, payment=payment, is_takeaway=is_takeaway)
#
#         total_sum = 0
#         for cart_item in cart_items:
#             total_sum += cart_item.dish.price * cart_item.quantity
#             OrderItem.objects.create(order=order, dish=cart_item.dish, quantity=cart_item.quantity)
#             cart_item.delete()
#
#         cart.delete()
#
#         order.total_price = total_sum
#         order.save()
#         serializer = OrderSerializer(order)
#         return Response(serializer.data)