from django.contrib import admin

from users.models import User, UserLog, SellerStatistics, UserInteractionEvent, Notification, Feedback, SellerProfile

admin.site.register(User)
admin.site.register(SellerProfile)
admin.site.register(Notification)
admin.site.register(Feedback)
admin.site.register(UserInteractionEvent)
admin.site.register(UserLog)
admin.site.register(SellerStatistics)