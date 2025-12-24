from django.db import models
from django.contrib.auth.models import User


# Model for Category
class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name')
    slug = models.SlugField(unique=True)  # We use it for pretty URLs : falco.com/hair/

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


# Model for Product
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name='Category')
    name = models.CharField(max_length=30, blank=True, null=True, verbose_name='Name')
    description = models.TextField(max_length=500, blank=True, verbose_name='Description')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Price')
    stock = models.IntegerField(blank=True, null=True, verbose_name='Stock')
    image_product = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Imagen')
    is_active = models.BooleanField(blank=True, null=True, verbose_name='Is_active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name 


# Model for Order
class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE, verbose_name='User')
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('paid', 'Pagado'),
        ('shipped', 'Enviado'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Pedido {self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name='Quantity')
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"