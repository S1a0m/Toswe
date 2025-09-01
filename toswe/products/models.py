from datetime import datetime

from django.db import models


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
    quantity_stock = models.PositiveIntegerField()
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
    is_main_image = models.BooleanField(default=False, unique=True)

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

    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Ad(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    pass

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

    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="payments")
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
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
    rating = models.PositiveIntegerField(default=5)
    comment = models.TextField(blank=True)
    is_verified_purchase = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)