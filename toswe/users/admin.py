from django.contrib import admin

from users.models import CustomUser, UserLog, SellerStatistics, UserInteractionEvent, Notification, SellerProfile

admin.site.register(CustomUser)
admin.site.register(Notification)
admin.site.register(UserInteractionEvent)
admin.site.register(UserLog)
admin.site.register(SellerStatistics)

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "shop_name", "is_verified", "is_premium", "is_brand", "show_on_market", "premium_expires_at")
    list_filter = ("is_verified", "is_premium", "is_brand")
    search_fields = ("user__username", "shop_name")

    fieldsets = (
        ("Informations Boutique", {
            "fields": ("user", "shop_name", "slogan", "about", "categories", "show_on_market", "subscribers"),
        }),
        ("Documents", {
            "fields": ("logo", "id_card", "commercial_register", "is_verified")
        }),
        ("Statuts", {
            "fields": ("is_premium", "is_brand", "premium_expires_at")
        }),
    )