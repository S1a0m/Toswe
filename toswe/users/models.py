from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AnonymousUser
from django.db import models

from django.utils import timezone
from products.models import Product, Category

from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    """
    Manager personnalisé pour le modèle CustomUser
    utilisant le champ `phone` comme identifiant principal
    """

    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Le numéro de téléphone est obligatoire")

        # Normalisation possible (ex: +33, etc.)
        phone = str(phone).strip()
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not password:
            raise ValueError("Le mot de passe est obligatoire pour le superuser")

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Le superuser doit avoir is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Le superuser doit avoir is_superuser=True.")

        return self.create_user(phone, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    session_mdp = models.CharField(max_length=6, blank=True, null=True)
    mdp_timeout = models.DateTimeField(blank=True, null=True)
    last_authenticated = models.DateTimeField(blank=True, null=True)

    username = models.CharField(blank=True, max_length=150, verbose_name='pseudo')
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    is_seller = models.BooleanField(default=False)


    objects = CustomUserManager()
    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class SellerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="seller_profile")
    shop_name = models.CharField(default='', max_length=100, null=True, blank=True)
    logo = models.ImageField(upload_to="logo", null=True, blank=True)
    subscribers = models.ManyToManyField(CustomUser, related_name="subscriptions", blank=True)

    categories = models.ManyToManyField(Category, related_name="categories", blank=True)

    slogan = models.CharField(max_length=255, default="")
    about = models.TextField(blank=True)

    commercial_register = models.FileField(upload_to="commercial_register", null=True, blank=True)
    id_card = models.FileField(upload_to="id_card", null=True, blank=True)

    is_brand = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)  # Registre de commerce verifie
    is_premium = models.BooleanField(default=False)

    show_on_market = models.BooleanField(default=False)

    rating = models.FloatField(default=0)

    force_payment = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class ProductsPreferences(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)


class UserLog(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="log")
    total_views = models.PositiveIntegerField(default=0)
    total_clicks = models.PositiveIntegerField(default=0)
    total_searches = models.PositiveIntegerField(default=0)
    total_add_to_cart = models.PositiveIntegerField(default=0)
    total_purchases = models.PositiveIntegerField(default=0)

    last_product_viewed = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL,
                                            related_name="last_viewed_by")
    last_search_query = models.CharField(max_length=255, blank=True, null=True)
    last_activity = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Log for {self.user.racine_id}"


class SellerStatistics(models.Model):
    seller = models.OneToOneField(SellerProfile, on_delete=models.CASCADE, related_name="stats", blank=True, null=True)
    total_views = models.PositiveIntegerField(default=0)
    total_products = models.PositiveIntegerField(default=0)
    total_orders = models.PositiveIntegerField(default=0)
    total_income = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    total_subscribers = models.PositiveIntegerField(default=0)
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    last_sale_date = models.DateTimeField(null=True, blank=True)
    best_selling_product_name = models.CharField(max_length=255, blank=True, null=True)
    best_selling_product_id = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Stats for Seller {self.seller.user.username}"


class UserInteractionEvent(models.Model):
    ACTION_CHOICES = [
        ('view', 'View'),
        ('click', 'Click'),
        ('search', 'Search'),
        ('cart', 'AddToCart'),
        ('buy', 'Buy')
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)
    details = models.JSONField(null=True, blank=True)


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255)
    message = models.TextField()
    # type = models.CharField(max_length=50)  # 'order', 'promo', 'system'
    detail_link = models.URLField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



