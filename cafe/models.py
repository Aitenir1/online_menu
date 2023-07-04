from django.db import models
import uuid

from cafe.Cheque import Cheque

from MotionWeb.settings.base import FONT_PATH

from sh import lp

class Table(models.Model):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.id}"

class Dish(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name_en = models.CharField(max_length=200)
    name_kg = models.CharField(max_length=200, default='Тамак')
    name_ru = models.CharField(max_length=200, default='Еда')
    description_en = models.TextField()
    description_kg = models.TextField(default='Тамак')
    description_ru = models.TextField(default='Еда')
    price = models.FloatField()
    gram = models.CharField(max_length=100, default='200')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ImageField(default='food1.png', upload_to='dishes/')

    def __str__(self):
        return f"{self.name_en} | {self.price}"


class Additive(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name_en = models.CharField(max_length=50)
    name_ru = models.CharField(max_length=50)
    name_kg = models.CharField(max_length=50)
    price = models.FloatField(default=0)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='available_additives')

    def __str__(self):
        return f"{self.dish.name_en} + {self.name_en}"


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):

    STATUS_CHOICES = (
        (0, 'In progress'),
        (1, 'Completed'),
    )

    TAKEAWAY_CHOICES = (
        (0, 'Here'),
        (1, 'Takeaway order'),
    )

    PAYMENT_CHOICES = (
        (0, 'Cash'),
        (1, 'Terminal')
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    table = models.ForeignKey('Table', on_delete=models.DO_NOTHING)
    time_created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    is_takeaway = models.IntegerField(choices=TAKEAWAY_CHOICES, default=0)
    payment = models.IntegerField(choices=PAYMENT_CHOICES, default=0)
    total_price = models.PositiveIntegerField(default=0, blank=True, null=True, editable=False)

    def __str__(self):
        return f"This order | {self.total_price}"

    def generate_cheque(self):
        cheque_pdf = Cheque(
            date=self.time_created.strftime("%d.%m.%y %H:%M:%S"),
            table=self.table,
            format=(50, 55 + 4 * len(self.items.all()))
        )

        cheque_pdf.add_page()
        # cheque.set_margins(1, 2, 2)
        # cheque.set_title("CHEQUE")
        # cheque.set_font("DejaVu", '', 7)
        cheque_pdf.set_font('DejaVu', style='', size=8)
        cheque_pdf.cell(0, 0.5, "---------------------------------------" * 2, 0, 1)
        cheque_pdf.cell(25, 4, "Блюда", 0, 0)
        cheque_pdf.cell(16, 4, "Кол.", 0, 0)
        cheque_pdf.cell(15, 4, "Сумма", 0, 1, 'C')

        cheque_pdf.set_font('DejaVu', style='', size=7)

        for order_item in self.items.all():
            dish_name = order_item.dish.name_ru

            if len(dish_name) > 18:
                dish_name = dish_name[:17] + '.'

            cheque_pdf.cell(25, 4, dish_name, 0, 0)
            cheque_pdf.cell(12, 4, f"{order_item.quantity}*{order_item.dish.price}", 0, 0)
            cheque_pdf.cell(11, 4, f"={order_item.quantity*order_item.dish.price}", 0, 1)

            for additive in order_item.additives.all():
                cheque_pdf.cell(50, 4, additive.name_ru, 0, 0)
                cheque_pdf.cell(10, 4, f"={additive.price}", 0, 1)
        cheque_pdf.cell(0, 0.5, "---------------------------------------" * 2, 0, 1)
        cheque_pdf.set_font("DejaVu", '', 10)
        print("IS SIOM")
        cheque_pdf.cell(0, 6, f"Общая сумма: {self.total_price}", 0, 1, "")
        cheque_pdf.output('cheque.pdf', 'F')

        lp('cheque.pdf')

        return cheque_pdf

    class Meta:
        ordering = ['status', 'time_created']

class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    additives = models.ManyToManyField(Additive, blank=True)
