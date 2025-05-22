from django.db import models

class Product(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField()
    plato = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='productos/')  # o URLField si solo tienes URL

    def __str__(self):
        return self.nombre
# Create your models here.
