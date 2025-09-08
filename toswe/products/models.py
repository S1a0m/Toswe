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
        ('new', 'New'),
        ('promo', 'Promo'),
        ('popular', 'Popular'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # quantity_stock = models.PositiveIntegerField()
    is_sponsored = models.BooleanField(default=False)
    is_promoted = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    seller = models.ForeignKey('users.SellerProfile', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(default=datetime.now)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        return self.name

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

class ProductPromotion(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='promotions')
    poster = models.ImageField(upload_to='promotions/', blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    ended_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.product.seller.shop_name

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
    title = models.CharField(max_length=255, default='')
    description = models.TextField(blank=True, null=True)
    product = models.ForeignKey("Product", related_name="ads", on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='ads/', blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

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