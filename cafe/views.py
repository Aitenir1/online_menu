from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.shortcuts import render, redirect, HttpResponse
from django.utils.dateparse import parse_date

from rest_framework import viewsets, generics

from cafe.models import Dish, Order
from cafe.serializers import DishSerializer, OrderSerializer


class DishViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer


class OrderCreateApi(generics.CreateAPIView):
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
            if date is not None and len(date) > 5:
                date = parse_date(date)
                return queryset.filter(time_created__date=date)

        return queryset.filter(status=0)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        if queryset:
            context['date'] = queryset.first().time_created

        return context


def complete_order(request, pk):
    if request.method == 'POST':
        order = Order.objects.get(id=pk)
        order.status = 1
        order.save()

        return redirect('home')

    return render(request, 'complete_order.html')


def get_cheque(request, pk):
    order = Order.objects.get(id=pk)
    cheque = order.generate_cheque()
    response = HttpResponse(content_type='application/pdf')
    response["Content-Disposition"] = f"attachment; filename=cheque_order_{str(order.id)[:5]}.pdf"
    response.write(cheque.output(dest="S").encode('latin-1'))

    return response
