from django.contrib import admin
from .models import Dish, Table, Category, Order, Cart

# Register your models here.
admin.site.register(Dish)
admin.site.register(Table)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Cart)
