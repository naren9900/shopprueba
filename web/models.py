from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)#EVITAR INCONSISTENCIA DE DATO
    name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    registration_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='Productos', blank=True)

    def __str__(self):
        return self.name


class Client(models.Model):
    user_id = models.OneToOneField(User, on_delete = models.RESTRICT)
    dni = models.CharField(max_length=8)
    sexo = models.CharField(max_length=1, default='M')
    telefono = models.CharField(max_length=20)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    direccion = models.TextField(null=True)

    def __str__(self):
        return self.dni


class SaleOrder(models.Model):
    STATE_CHOICES = (
        ('draft', 'Borrador'),
        ('cancelled', 'Cancelado'),
        ('done', 'Hecho'),
        ('paid', 'Pagado'),
    )
    client = models.ForeignKey(Client, on_delete=models.RESTRICT)
    registration_date = models.DateTimeField(auto_now_add=True)
    order_number = models.CharField(max_length=20, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    state = models.CharField(max_length=11, default='draft', choices=STATE_CHOICES)

    def __str__(self):
        return self.order_number


class SaleOrderLine(models.Model):
    sale_order = models.ForeignKey(SaleOrder, on_delete=models.RESTRICT)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    amount = models.IntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product.name

