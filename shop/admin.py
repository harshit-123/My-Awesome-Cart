from django.contrib import admin
from .models import Product, Contact, Order, OrderUpdate
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    fields = ('product_name', 'desc', 'category', 'image', 'price', 'sub_category','published_date')
    list_display = ['product_name','category','price','sub_category']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id','name','amount','email', 'zip', 'city', 'state']

admin.site.register(Product, ProductAdmin)
admin.site.register(Contact)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderUpdate)