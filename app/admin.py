from django.contrib import admin
from .models import Customer, Product, Order, Tag


# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'product', 'status')
    list_filter = ('status', 'date_created')
    search_fields = ('customer__name', 'product__name')


admin.site.register(Order, OrderAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'address')
    search_fields = ('name', 'email', 'phone', 'address')


admin.site.register(Customer, CustomerAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'description')
    list_filter = ('category', 'date_created')
    search_fields = ('name', 'category', 'description')


admin.site.register(Product, ProductAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Tag, TagAdmin)