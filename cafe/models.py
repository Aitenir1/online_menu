from django.db import models

class Dish(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.name} | {self.price}"


class Table(models.Model):
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"Table #{self.id}"


class Customer(models.Model):
    name = models.CharField(max_length=200)
    table = models.ForeignKey('Table', on_delete=models.CASCADE)


class Cart(models.Model):
    dishes = models.ManyToManyField('Dish')

    def __str__(self):
        return f"{', '.join([dish.name for dish in self.dishes.all()])}"

class Order(models.Model):
    STATUS_CHOICES = (
        (0, 'In progress'),
        (1, 'Completed'),
    )

    cart = models.OneToOneField('Cart', on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)

    def __str__(self):
        return f"{sum([dish.price for dish in self.cart.dishes.all()])}"
