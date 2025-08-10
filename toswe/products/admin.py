from django.contrib import admin

from products.models import Product, Category, Cart, CartItem, Order, OrderItem, Payment, Delivery

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Delivery)
