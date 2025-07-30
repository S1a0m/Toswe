from django.contrib import admin

from users.models import Client, Seller, Notification, User

admin.site.register(User)
admin.site.register(Client)
admin.site.register(Seller)
admin.site.register(Notification)