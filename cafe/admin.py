from django.contrib import admin
from .models import Dish, Table, Customer, Order, Cart

# Register your models here.
admin.site.register(Dish)
admin.site.register(Table)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Cart)
