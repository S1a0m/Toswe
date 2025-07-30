from django.contrib import admin

from products.models import Category, Payment, Delivery, Feedback, Product

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Payment)
admin.site.register(Delivery)
admin.site.register(Feedback)
