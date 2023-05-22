from django.urls import path, include
from rest_framework import routers
from cafe.views import DishViewSet, OrderViewSet, MyLoginView, OrderListView, complete_order

from django.contrib.auth.decorators import login_required

router = routers.DefaultRouter()
router.register(r'dishes', DishViewSet, basename='dish')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/orders', OrderViewSet.as_view()),
    path('login/', MyLoginView.as_view(), name='login'),
    path('home/', login_required(OrderListView.as_view()), name='home'),
    path('complete_order/<str:pk>', login_required(complete_order), name='complete_order'),
    *router.urls
]