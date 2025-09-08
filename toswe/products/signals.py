# signals.py
import qrcode
from io import BytesIO
from django.core.files import File
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core import signing
from .models import Product

from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import Order
#from users.models import Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from toswe.utils import generate_order_pdf

@receiver(post_save, sender=Product)
def generate_qr_code(sender, instance, created, **kwargs):
    if created and not instance.qr_code:
        # On signe juste l'ID du produit
        signed_id = signing.dumps(instance.id)

        # URL finale avec signature
        qr_url = f"{settings.FRONTEND_URL}/scan-product/{signed_id}"

        # Génération du QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(qr_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Sauvegarde image
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        filename = f"{instance.id}_qr.png"
        instance.qr_code.save(filename, File(buffer), save=False)
        instance.save(update_fields=['qr_code'])


@receiver(post_save, sender=Order)
def order_created_notification(sender, instance, created, **kwargs):
    if created:
        # Génération du PDF
        pdf_file = generate_order_pdf(instance)
        filename = f"order_{instance.id}.pdf"
        instance.pdf.save(filename, pdf_file, save=True)

        # Notification (si tu en as besoin)
        #Notification.objects.create(
            #user=instance.user,
            #message=f"Votre commande #{instance.id} a été créée."
        #)

        # WebSocket si nécessaire
        #channel_layer = get_channel_layer()
        #async_to_sync(channel_layer.group_send)(
           # "notifications",
           # {"type": "send_notification", "message": f"Nouvelle commande #{instance.id}"}
        #)

