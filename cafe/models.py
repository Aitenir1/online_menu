from django.db import models
import uuid
from django.utils import timezone

from cafe.Cheque import Cheque

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
        # Create a PDF instance with smaller page size (e.g., 80mm x 150mm)
        cheque_pdf = Cheque(format=(80, 150))

        # Set document properties
        cheque_pdf.set_title("Cheque")
        cheque_pdf.set_auto_page_break(auto=True, margin=5)

        # Add a page
        cheque_pdf.add_page()

        # Set font and font size
        cheque_pdf.set_font("Arial", "", 10)

        # Add content to the cheque
        cheque_pdf.cell(0, 5, f"Date : {self.time_created.strftime('%d-%m-%y')}", 0, 1)
        cheque_pdf.cell(0, 5, f"Time : {self.time_created.strftime('%i-%h')}", 0, 1)
        cheque_pdf.cell(0, 5, f"Table: {self.table}", 0, 1)
        cheque_pdf.cell(0, 5, f"Total Amount: ${self.total_price}", 0, 1)

        # Save the PDF
        cheque_pdf.output("media/cheque.pdf")

    class Meta:
        ordering = ['status', 'time_created']

class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    dish = models.ForeignKey('Dish', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', related_name='items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)