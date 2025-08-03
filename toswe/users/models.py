from django.db import models
from django.utils import timezone

from toswe.products.models import Product


class User(models.Model):
    racine_id = models.CharField(max_length=255, unique=True)
    session_mdp = models.CharField(max_length=255, default='mdp')
    mdp_timeout = models.DateTimeField(null=True, blank=True)
    is_authenticated = models.BooleanField(default=False)
    is_online = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    is_brand = models.BooleanField(default=False)

    last_authenticated = models.DateTimeField(null=True, blank=True)

class UserLog(models.Model): # pour donner certains avantages aux clients les plus actifs
    user = models.OneToOneField(User, on_delete=models.CASCADE)

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
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    total_products = models.PositiveIntegerField(default=0)
    total_orders = models.PositiveIntegerField(default=0) # ne pas oublier pour evolution de vente
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

    def __str__(self):
        return f"{self.user.racine_id} - {self.action} - {self.timestamp}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    type = models.CharField(max_length=50)  # 'order', 'promo', 'system'
    detail_link = models.URLField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    sent_date = models.DateTimeField(auto_now_add=True)


class Feedback(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
