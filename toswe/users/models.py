from django.db import models
from django.contrib.auth.models import AbstractUser

class User(models.Model):
    racine_id = models.CharField(max_length=255, unique=True)

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_state = models.CharField(max_length=20, choices=[('basic', 'Basic'), ('premium', 'Premium')], default='basic')

class SellerStatistics(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pass

class ClientLog(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    type = models.CharField(max_length=50)  # e.g., 'order', 'promo', 'system'
    detail_link = models.URLField(null=True, blank=True)
    read = models.BooleanField(default=False)
    sent_date = models.DateTimeField(auto_now_add=True)

