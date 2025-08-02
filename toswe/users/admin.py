from django.contrib import admin

from users.models import User, Notification

admin.site.register(User)
admin.site.register(Notification)