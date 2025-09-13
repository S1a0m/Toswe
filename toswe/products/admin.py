from django.contrib import admin

from products.models import Product, Category, Cart, CartItem, Order, OrderItem, Payment, Delivery, ProductImage, Feedback, Promotion, Ad

admin.site.register(Product)
admin.site.register(Ad)
admin.site.register(Promotion)
admin.site.register(ProductImage)
admin.site.register(Feedback)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Delivery)
