from django.db import models
import uuid

from cafe.Cheque import Cheque

from django.utils import timezone

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
    gram = models.IntegerField(default=200)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ImageField(default='food1.png')

    def __str__(self):
        return f"{self.name_en} | {self.price}"


class Additive(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)

    def __str__(self):
        return self.dish.name_en + self.name

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
            format=(80, 100)
        )

        cheque_pdf.add_font('DejaVu', '', 'fonts/DejaVuSansCondensed.ttf', uni=True)
        cheque_pdf.set_font("DejaVu", '', 8)

        cheque_pdf.set_auto_page_break(auto=True, margin=5)
        cheque_pdf.add_page()

        cheque_pdf.cell(0, 5, 'Наименования товаров:', 0, 1)

        for order_item in self.items.all():
            cheque_pdf.cell(40, 4, order_item.dish.name_ru, 0, 0)
            cheque_pdf.cell(10, 4, f"{order_item.quantity}*{order_item.dish.price}", 0, 0)
            cheque_pdf.cell(10, 4, f"={order_item.quantity*order_item.dish.price}", 0, 1)

        cheque_pdf.cell(0, 5, "", 0, 1)
        cheque_pdf.cell(0, 4, f"Наличными", 0, 1, "")
        cheque_pdf.set_font("DejaVu", '', 10)
        cheque_pdf.cell(0, 4, f"Общая сумма: {self.total_price}", 0, 1, "")

        return cheque_pdf
        # cheque_pdf.output(f"cheque_{str(self.id)[:5]}.pdf")

    class Meta:
        ordering = ['status', 'time_created']

class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)