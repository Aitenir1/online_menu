from django.urls import path, include
from rest_framework import routers
from cafe.views import DishViewSet, OrderCreateApi, MyLoginView, \
    OrderListView, complete_order, get_cheque

from django.contrib.auth.decorators import login_required


router = routers.DefaultRouter()
router.register(r'dishes', DishViewSet, basename='dish')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/orders', OrderCreateApi.as_view()),
    path('login/', MyLoginView.as_view(), name='login'),
    path('home/', login_required(OrderListView.as_view()), name='home'),
    path('complete_order/<str:pk>', login_required(complete_order), name='complete_order'),
    path('get_cheque/<str:pk>', login_required(get_cheque), name='get_cheque'),
    *router.urls
]