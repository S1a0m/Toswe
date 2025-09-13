from datetime import datetime

from django.db import models

from django.utils import timezone
# from users.models import CustomUser


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    STATUS_CHOICES = [
        ("new", "New"),
        ("popular", "Popular"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveIntegerField()

    seller = models.ForeignKey("users.SellerProfile", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="new")

    is_online = models.BooleanField(default=True)

    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def active_promotions(self):
        """Retourne les promotions encore valides"""
        return self.promotions.filter(ended_at__gte=timezone.now())

    @property
    def active_ads(self):
        """Retourne les publicités actives (sponsorisées ou non)"""
        return self.ads.filter(is_active=True, ended_at__gte=timezone.now())

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_main_image = models.BooleanField(default=False)

    def __str__(self):
        return f"Image de {self.product.name}"

class ProductVideo(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='videos')
    video = models.FileField(upload_to='videos/')

    def __str__(self):
        return f"Video de {self.product.name}"

class Promotion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='promotions')
    discount_percent = models.PositiveIntegerField(null=True, blank=True)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now)
    ended_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Si le vendeur renseigne seulement le pourcentage → calcul du prix réduit
        if self.discount_percent and not self.discount_price:
            self.discount_price = self.product.price * (1 - (self.discount_percent / 100))

        # Si le vendeur renseigne un prix → on peut recalculer le pourcentage
        elif self.discount_price and not self.discount_percent:
            self.discount_percent = round(
                100 - (self.discount_price * 100 / self.product.price)
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Promo de {self.product.name} ({self.discount_percent}% off)"


class Cart(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart de {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Produit {self.product.name}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ]

    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    phone_number = models.CharField(max_length=20, default='')
    contact_method = models.CharField(
        max_length=20,
        choices=[("whatsapp", "WhatsApp"), ("call", "Appel")],
        default="call"
    )
    address = models.TextField(default='')

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    pdf = models.FileField(upload_to="orders/pdf/", null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id} - {self.phone_number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Ad(models.Model):
    AD_TYPE_CHOICES = [
        ("generic", "Annonce Générale"),
        ("sponsored", "Sponsorisation Produit"),
    ]

    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    product = models.ForeignKey(
        Product, related_name="ads", on_delete=models.CASCADE, blank=True, null=True
    )
    image = models.ImageField(upload_to="ads/", blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    ad_type = models.CharField(max_length=20, choices=AD_TYPE_CHOICES, default="generic")
    is_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_ad_type_display()} ({self.id})"


# models.py
class Payment(models.Model):
    PAYMENT_METHODS = [
        ("mtn_momo", "MTN MoMo"),
        ("moov_money", "Moov Money"),
    ]

    PAYMENT_TYPES = [
        ("order", "Order Payment"),
        ("premium", "Premium Subscription"),
        ("sponsorship", "Product Sponsorship"),
        ("advertisement", "Advertisement"),
    ]

    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="payments", blank=True, null=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES, default='order')
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    # relationnels optionnels selon type de paiement
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)  # pour sponsorisation
    advertisement = models.OneToOneField(Ad, on_delete=models.CASCADE, null=True, blank=True)

    paid_at = models.DateTimeField(auto_now_add=True)
    is_successful = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.payment_type} - {self.amount} CFA"


class Delivery(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    address = models.TextField()
    contact_phone = models.CharField(max_length=20)
    delivered = models.BooleanField(default=False)
    delivery_date = models.DateTimeField(null=True, blank=True)


class Feedback(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey('users.CustomUser', on_delete=models.SET_NULL, null=True)
    rating = models.FloatField(default=0)
    comment = models.TextField(blank=True)
    is_verified_purchase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)