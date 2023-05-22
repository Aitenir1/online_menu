from django.contrib import admin
from .models import Dish, Table, Category, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('dish',)


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'table', 'get_dishes', 'total_price')

    def get_dishes(self, obj):
        # Retrieve the list of dishes associated with the order
        dishes = Dish.objects.filter(orderitem__order=obj)
        dish_names = ', '.join([dish.name_en for dish in dishes])
        return dish_names

    get_dishes.short_description = 'Dishes'


# Register your models here.
admin.site.register(Dish)
admin.site.register(Table)
admin.site.register(Category)
admin.site.register(Order, OrderAdmin)
# admin.site.register(Cart)
# admin.site.register(CartItem)
admin.site.register(OrderItem)
