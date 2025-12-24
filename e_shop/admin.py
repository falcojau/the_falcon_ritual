from django.contrib import admin
# Register your models here.
from e_shop.models import Product, Category, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['category', 'name',
                    'description', 'price',
                    'stock', 'image_product',
                    'is_active','created_at']
    list_filter = ['category', 'name',
                    'stock', 'is_active','created_at']
    search_fields = ['category', 'name', 'is_active']
    ordering = ['-price']

# This allows to see the items inside Order
class OrderItemInline(admin.TabularInline):
    model = OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'id']
    inlines = [OrderItemInline]