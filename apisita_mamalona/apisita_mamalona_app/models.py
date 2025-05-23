from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Product(models.Model):
    name = models.CharField(max_length=255)  # Renamed from nombre
    description = models.TextField()  # Renamed from descripcion
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Renamed from precio
    image = models.URLField(blank=True)  # Renamed from imagen
    category = models.CharField(max_length=100)  # Renamed from plato

    def __str__(self):
        return self.name  # Updated to use self.name

class Order(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    ccn = models.CharField(max_length=16, blank=True, null=True)
    exp = models.CharField(max_length=5, blank=True, null=True)
    cvv = models.CharField(max_length=4, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    state = models.CharField(max_length=50)

    products = models.ManyToManyField(Product, through='OrderProduct')

    def __str__(self):
        return f"Order #{self.id} - {self.name}"

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in Order #{self.order.id}"  # Updated to use self.product.name