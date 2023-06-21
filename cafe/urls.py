from django.urls import path, include
from django.contrib.auth.decorators import login_required

from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from cafe.views import (
    DishViewSet,
    OrderCreateApi,
    OrderListApiView,
    MyLoginView,
    OrderListView,
    OrderStatusApiView,
    complete_order,
    get_cheque
)

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = routers.DefaultRouter()
router.register(r'dishes', DishViewSet, basename='dish')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/orders', OrderCreateApi.as_view()),
    path('api/orders-get/', OrderListApiView.as_view(), name='order-create'),
    path('api-token-auth/', obtain_auth_token, name='get-token'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('home/', login_required(OrderListView.as_view()), name='home'),
    path('api/order/<str:pk>/status', OrderStatusApiView.as_view(), name='order-status'),
    path('complete_order/<str:pk>', login_required(complete_order), name='complete_order'),
    path('get_cheque/<str:pk>', login_required(get_cheque), name='get_cheque'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
    *router.urls,
]