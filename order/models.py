from django.contrib.auth.models import User
from django.db import models
from product.models import Product

class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE, verbose_name="User")
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, verbose_name="Last Name")
    email = models.EmailField(max_length=100, verbose_name="Email Address")  # Cambiado a EmailField para validación de correos
    address = models.CharField(max_length=100, verbose_name="Address")
    zipcode = models.CharField(max_length=20, verbose_name="Zip Code")  # Ajustado para permitir códigos postales más largos
    place = models.CharField(max_length=100, verbose_name="Place")
    phone = models.CharField(max_length=20, verbose_name="Phone Number")  # Ajustado para formatos de teléfono más largos
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name="Paid Amount")
    stripe_token = models.CharField(max_length=255, verbose_name="Stripe Token")  # Aumentado el tamaño para token más largo

    class Meta:
        ordering = ['-created_at',]
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="Order")
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name="Product")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Price")
    quantity = models.IntegerField(default=1, verbose_name="Quantity")

    def __str__(self):
        return f'Order {self.order.id} - Product {self.product.name}'
