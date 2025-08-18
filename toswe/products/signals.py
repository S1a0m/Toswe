# signals.py
import qrcode
from io import BytesIO
from django.core.files import File
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core import signing
from .models import Product

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

