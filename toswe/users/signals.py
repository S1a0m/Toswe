# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Notification
from products.models import Order
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@receiver(post_save, sender=Order)
def order_created_notification(sender, instance, created, **kwargs):
    if created:
        # Si l'utilisateur est connecté → notification pour lui
        if instance.user:
            notif = Notification.objects.create(
                user=instance.user,
                message="Votre commande a été enregistrée."
            )

            # Envoi en temps réel au client connecté
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{instance.user.id}",
                {
                    "type": "send_notification",
                    "message": notif.message,
                    "timestamp": str(notif.created_at),
                }
            )

        # Notification admin (par exemple tous les superusers)
        from django.contrib.auth import get_user_model
        User = get_user_model()
        admins = User.objects.filter(is_staff=True)
        for admin in admins:
            notif = Notification.objects.create(
                user=admin,
                message=f"Nouvelle commande #{instance.id} créée."
            )
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{admin.id}",
                {
                    "type": "send_notification",
                    "message": notif.message,
                    "timestamp": str(notif.created_at),
                }
            )

        # Notification pour chaque vendeur concerné
        print("Order items:", instance.items.all())
        print("Seller IDs (raw):", list(instance.items.values_list("product__seller_id", flat=True)))
        print("Seller IDs (relation):", list(instance.items.values_list("product__seller__id", flat=True)))
        print("Products:", list(instance.items.values_list("product__name", flat=True)))

        seller_ids = (
            instance.items.values_list("product__seller__id", flat=True).distinct()
        )
        print("Les sellers sont dans la liste des products:", seller_ids)
        from users.models import SellerProfile
        sellers = SellerProfile.objects.filter(id__in=seller_ids)
        print("Les vendeurs: ", sellers)
        for seller in sellers:
            notif = Notification.objects.create(
                user=seller.user,
                message=f"Nouvelle commande contenant vos produits (commande #{instance.id})."
            )
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{seller.user.id}",
                {
                    "type": "send_notification",
                    "message": notif.message,
                    "timestamp": str(notif.created_at),
                }
            )
