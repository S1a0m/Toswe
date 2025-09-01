from django.contrib import admin

from users.models import CustomUser, UserLog, SellerStatistics, UserInteractionEvent, Notification, SellerProfile

admin.site.register(CustomUser)
admin.site.register(Notification)
admin.site.register(UserInteractionEvent)
admin.site.register(UserLog)
admin.site.register(SellerStatistics)

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "shop_name", "is_verified", "is_premium", "is_brand")
    list_filter = ("is_verified", "is_premium", "is_brand")
    search_fields = ("user__username", "shop_name")

    fieldsets = (
        ("Informations Boutique", {
            "fields": ("user", "shop_name", "slogan", "about", "categories")
        }),
        ("Documents", {
            "fields": ("logo", "id_card", "commercial_register", "is_verified")
        }),
        ("Statuts", {
            "fields": ("is_premium", "is_brand")
        }),
    )