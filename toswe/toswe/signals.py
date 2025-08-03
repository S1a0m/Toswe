# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from toswe.users.models import Order, Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver(post_save, sender=Order)
def order_created_notification(sender, instance, created, **kwargs):
    if created:
        notif = Notification.objects.create(
            user=instance.user,
            message="Votre commande a été enregistrée."
        )

        # Envoi en temps réel
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"user_{instance.user.id}",  # nom du groupe WebSocket
            {
                "type": "send_notification",
                "message": notif.message,
            }
        )

