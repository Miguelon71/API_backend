from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Product(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.URLField(blank=True)
    plato = models.CharField(max_length=100)  # asumido como categoría/plato

    def __str__(self):
        return self.nombre

class Order(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    ccn = models.CharField(max_length=16)
    exp = models.CharField(max_length=5)
    cvv = models.CharField(max_length=4)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    state = models.CharField(max_length=50)

    products = models.ManyToManyField(Product, through='OrderProduct')

    def _str_(self):
        return f"Order #{self.id} - {self.name}"

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def _str_(self):
        return f"{self.quantity}x {self.product.name} in Order #{self.order.id}"