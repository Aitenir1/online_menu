from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import action

from cafe.models import Dish, Order
from cafe.serializers import DishSerializer, OrderSerializer
# from .Forms import OrderForm

from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic import ListView
from django.views.generic.edit import FormView

from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, reverse

from django.utils.dateparse import parse_date

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

        if self.request.method == "GET":
            date = self.request.GET.get('date')
            # print(type(date))
            # print(date.year)
            if date is not None:
                # year, month, day = date.split('-')
                date = parse_date(date)
                return queryset.filter(time_created__date=date)

        return queryset.filter(status=0)


class OrderSearchView(ListView):
    model = Order
    # form_class = OrderForm
    template_name = 'search.html'

    def get_queryset(self):
        if self.request.method == "GET":
            date = self.request.GET.get('date')
            # print(type(date))
            # print(date.year)
            if date is not None:
                # year, month, day = date.split('-')
                date = parse_date(date)
                # print(date)
                print(Order.objects.filter(time_created__date=date))
        return super().get_queryset()


def complete_order(request, pk):
    if request.method == 'POST':
        order = Order.objects.get(id=pk)
        print(order.time_created)
        order.status = 1
        # cheque = order.generate_cheque()
        order.save()

        # response = HttpResponse(content_type='application/pdf')
        # response["Content-Disposition"] = f"attachment; filename=cheque_order_{str(order.id)[:5]}.pdf"
        # response.write(cheque.output(dest="S").encode("latin-1"))

        return redirect('home')

    return render(request, 'complete_order.html')


def get_cheque(request, pk):
    order = Order.objects.get(id=pk)
    cheque = order.generate_cheque()
    print("афывоаыфод")
    response = HttpResponse(content_type='application/pdf')
    response["Content-Disposition"] = f"attachment; filename=cheque_order_{str(order.id)[:5]}.pdf"
    response.write(cheque.output(dest="S").encode('latin-1'))

    return response