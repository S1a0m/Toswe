import jwt

from toswe import settings
from users.models import CustomUser, UserInteractionEvent
from twilio.rest import Client
from django.conf import settings

import io, os
from django.conf import settings
from django.core.files.base import ContentFile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def generate_order_pdf(order):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # === Bandeau supérieur (fond couleur) ===
    p.setFillColor(colors.HexColor("#7D260F"))
    p.rect(0, height - 120, width, 120, fill=1)

    # === Logo blanc ===
    logo_path = os.path.join(settings.MEDIA_ROOT, "logo", "logo.png")
    if os.path.exists(logo_path):
        p.drawImage(logo_path, 50, height - 110, width=100, height=80, mask="auto")

    # === Titre Facture ===
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 22)
    p.drawRightString(width - 50, height - 60, f"Facture #{order.id}")

    p.setFont("Helvetica", 11)
    p.drawRightString(width - 50, height - 85, f"Date : {order.created_at.strftime('%d/%m/%Y %H:%M')}")

    # === Infos client ===
    y = height - 160
    p.setFillColor(colors.black)
    p.setFont("Helvetica-Bold", 13)
    p.drawString(50, y, "Informations Client")
    p.setFont("Helvetica", 11)
    p.drawString(50, y - 20, f"Téléphone : {order.phone_number}")
    p.drawString(50, y - 40, f"Méthode de contact : {order.contact_method}")
    p.drawString(50, y - 60, f"Adresse : {order.address}")
    p.drawString(50, y - 80, f"Statut : {dict(order.STATUS_CHOICES).get(order.status, 'Inconnu')}")

    # === Tableau des produits ===
    y -= 120
    styles = getSampleStyleSheet()
    data = [["Produit", "Quantité", "Prix unitaire", "Total ligne"]]

    total_general = 0
    for idx, item in enumerate(order.items.all()):
        total_ligne = item.quantity * float(item.price)
        total_general += total_ligne
        data.append([
            Paragraph(item.product.name, styles["Normal"]),
            str(item.quantity),
            f"{float(item.price):,.0f} Fcfa",
            f"{total_ligne:,.0f} Fcfa"
        ])

    # Ajouter total général
    data.append(["", "", Paragraph("<b>Total</b>", styles["Normal"]), f"{total_general:,.0f} Fcfa"])

    table = Table(data, colWidths=[8*cm, 3*cm, 3*cm, 3*cm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#7D260F")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 12),

        # Alternance gris clair/blanc
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.whitesmoke, colors.lightgrey]),

        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#EEE")),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("TEXTCOLOR", (0, -1), (-1, -1), colors.black),

        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))

    table.wrapOn(p, width, height)
    table.drawOn(p, 50, y)

    # === Footer stylé ===
    p.setFont("Helvetica-Oblique", 9)
    p.setFillColor(colors.HexColor("#7D260F"))
    p.drawCentredString(width / 2, 40, "Merci d'avoir commandé avec Tôswè ❤️")
    p.setFillColor(colors.black)
    p.setFont("Helvetica", 8)
    p.drawCentredString(width / 2, 28, "Tôswè - Nous vendons pour vous.")

    p.showPage()
    p.save()

    buffer.seek(0)
    return ContentFile(buffer.read(), name=f"order_{order.id}.pdf")



def send_sms(phone_number: str, message: str):
    """
    Envoie un SMS via Twilio.
    """
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        sms = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,  # Ton numéro Twilio
            to=phone_number,
        )
        return {"status": "success", "sid": sms.sid}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


def verify_token(token):
    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return {"authenticated": True, "detail": decoded}

    except jwt.ExpiredSignatureError:
        try:
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'], options={"verify_exp": False})
            user_id = decoded.get("user_id")
            user = CustomUser.objects.filter(id=user_id).first()
            if user:
                user.is_authenticated = False
                user.save()
        except Exception:
            pass
        return {"authenticated": False, "detail": "Token expiré"}

    except jwt.InvalidTokenError:
        return {"authenticated": False, "detail": "Token invalide"}

def track_user_interaction(user, product=None, action='view', details=None):
    if user and user.is_authenticated:
        UserInteractionEvent.objects.create(
            user=user,
            product=product,
            action=action,
            details=details or {}
        )


def is_eligible_to_be_seller(user):
    return (
        user.is_authenticated and
        user.phone_number and
        user.address
    )
