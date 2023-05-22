from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action

from cafe.models import Dish, Order
from cafe.serializers import DishSerializer, OrderSerializer

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import ListView

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