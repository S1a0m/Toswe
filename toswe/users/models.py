from django.db import models
from django.utils import timezone
from products.models import Product

class User(models.Model):
    racine_id = models.CharField(max_length=255, unique=True)
    is_authenticated = models.BooleanField(default=False)
    is_online = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    is_brand = models.BooleanField(default=False)

    slogan = models.CharField(max_length=255, default="")
    about = models.TextField(blank=True)

    last_authenticated = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.racine_id


class SellerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="seller_profile")
    loyal_customers = models.ManyToManyField(User, related_name="loyal_customers")

    def __str__(self):
        return self.user.racine_id


class UserLog(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="log")
    total_views = models.PositiveIntegerField(default=0)
    total_clicks = models.PositiveIntegerField(default=0)
    total_searches = models.PositiveIntegerField(default=0)
    total_add_to_cart = models.PositiveIntegerField(default=0)
    total_purchases = models.PositiveIntegerField(default=0)

    last_product_viewed = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL, related_name="last_viewed_by")
    last_search_query = models.CharField(max_length=255, blank=True, null=True)
    last_activity = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Log for {self.user.racine_id}"


class SellerStatistics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="stats")
    total_products = models.PositiveIntegerField(default=0)
    total_orders = models.PositiveIntegerField(default=0)
    total_income = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    last_sale_date = models.DateTimeField(null=True, blank=True)
    best_selling_product_name = models.CharField(max_length=255, blank=True, null=True)
    best_selling_product_id = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Stats for Seller {self.user.racine_id}"


class UserInteractionEvent(models.Model):
    ACTION_CHOICES = [
        ('view', 'View'),
        ('click', 'Click'),
        ('search', 'Search'),
        ('cart', 'AddToCart'),
        ('buy', 'Buy')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)
    details = models.JSONField(null=True, blank=True)


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    type = models.CharField(max_length=50)  # 'order', 'promo', 'system'
    detail_link = models.URLField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Feedback(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField(blank=True)
    is_verified_purchase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
