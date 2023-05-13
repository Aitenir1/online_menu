from django.db import models
import uuid

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
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING)
    image = models.ImageField(default='food1.png')

    def __str__(self):
        return f"{self.name_en} | {self.price}"


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Table(models.Model):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"Table #{self.id}"


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    dishes = models.ManyToManyField('Dish')

    def __str__(self):
        return f"{', '.join([dish.name_en for dish in self.dishes.all()])}"

class Order(models.Model):

    STATUS_CHOICES = (
        (0, 'In progress'),
        (1, 'Completed'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    cart = models.OneToOneField('Cart', on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    table = models.ForeignKey('Table', on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"{self.cart} {sum([dish.price for dish in self.cart.dishes.all()])}"
