import jwt

from toswe import settings
from users.models import CustomUser, UserInteractionEvent
from twilio.rest import Client
from django.conf import settings
from django.core.mail import send_mail

import io, os, qrcode
from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
from django.conf import settings
from django.core.files.base import ContentFile
 
def generate_order_pdf(order):
    import io, os
    import qrcode
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import Table, TableStyle, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.pdfgen import canvas
    from django.conf import settings
    from django.core.files.base import ContentFile
 
    buffer = io.BytesIO()
    p      = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    styles = getSampleStyleSheet()
 
    # ── Couleurs Tôswè ────────────────────────────────────────
    BRAND   = colors.HexColor("#7D260F")
    ACCENT  = colors.HexColor("#C65A2E")
    LIGHT   = colors.HexColor("#FDF7F2")
    GREY    = colors.HexColor("#F0EBE6")
 
    # ════════════════════════════════════════════════════════
    # HEADER — Bandeau couleur + logo + titre
    # ════════════════════════════════════════════════════════
    p.setFillColor(BRAND)
    p.rect(0, height - 110, width, 110, fill=1, stroke=0)
 
    # Logo
    logo_path = os.path.join(settings.MEDIA_ROOT, "logo", "logo.png")
    if os.path.exists(logo_path):
        p.drawImage(logo_path, 40, height - 100, width=90, height=75, mask="auto")
 
    # Titre et numéro
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 24)
    p.drawRightString(width - 40, height - 55, f"Facture #{order.id}")
    p.setFont("Helvetica", 11)
    p.drawRightString(width - 40, height - 75, f"Date : {order.created_at.strftime('%d/%m/%Y à %H:%M')}")
    p.setFont("Helvetica-Oblique", 9)
    p.drawRightString(width - 40, height - 92, "toswe-africa.com")
 
    # ════════════════════════════════════════════════════════
    # SECTION INFOS CLIENT + LIVRAISON
    # ════════════════════════════════════════════════════════
    y = height - 140
 
    # Fond carte info
    p.setFillColor(LIGHT)
    p.roundRect(35, y - 110, (width - 70) / 2 - 10, 110, 8, fill=1, stroke=0)
    p.roundRect(35 + (width - 70) / 2 + 10, y - 110, (width - 70) / 2 - 10, 110, 8, fill=1, stroke=0)
 
    # Colonne gauche — Client
    p.setFillColor(BRAND)
    p.setFont("Helvetica-Bold", 11)
    p.drawString(45, y - 15, "INFORMATIONS CLIENT")
    p.setFillColor(colors.black)
    p.setFont("Helvetica", 10)
    lines_left = [
        f"Téléphone : {order.phone_number}",
        f"Contact   : {'WhatsApp' if order.contact_method == 'whatsapp' else 'Appel téléphonique'}",
        f"Statut    : {dict(order.STATUS_CHOICES).get(order.status, order.status).upper()}",
    ]
    if order.user:
        lines_left.insert(0, f"Client    : {order.user.username}")
    for i, line in enumerate(lines_left):
        p.drawString(45, y - 32 - i * 17, line)
 
    # Colonne droite — Livraison
    col2_x = 40 + (width - 70) / 2 + 10
    p.setFillColor(BRAND)
    p.setFont("Helvetica-Bold", 11)
    p.drawString(col2_x + 10, y - 15, "LIVRAISON")
    p.setFillColor(colors.black)
    p.setFont("Helvetica", 10)
    delivery_label = "Livraison à domicile" if order.delivery_mode == "home" else "Retrait en point relais"
    lines_right = [
        f"Mode      : {delivery_label}",
        f"Ville     : {order.city or '—'}",
    ]
    if order.address_description:
        # Tronque si trop long
        addr = order.address_description
        lines_right.append(f"Adresse   : {addr[:45]}{'...' if len(addr) > 45 else ''}")
    for i, line in enumerate(lines_right):
        p.drawString(col2_x + 10, y - 32 - i * 17, line)
 
    # ════════════════════════════════════════════════════════
    # TABLEAU DES PRODUITS
    # ════════════════════════════════════════════════════════
    y -= 130
 
    p.setFillColor(BRAND)
    p.setFont("Helvetica-Bold", 12)
    p.drawString(40, y, "DÉTAIL DE LA COMMANDE")
    y -= 16
 
    # En-têtes
    data = [[
        Paragraph("<b>Produit</b>",       styles["Normal"]),
        Paragraph("<b>Boutique</b>",      styles["Normal"]),
        Paragraph("<b>Qté</b>",           styles["Normal"]),
        Paragraph("<b>Prix unit.</b>",    styles["Normal"]),
        Paragraph("<b>Total ligne</b>",   styles["Normal"]),
    ]]
 
    total_general = 0
    for item in order.items.all():
        total_ligne    = item.quantity * float(item.price)
        total_general += total_ligne
        shop_name      = item.product.seller.shop_name if hasattr(item.product, "seller") else "—"
        data.append([
            Paragraph(item.product.name,          styles["Normal"]),
            Paragraph(shop_name,                  styles["Normal"]),
            str(item.quantity),
            f"{float(item.price):,.0f} F",
            f"{total_ligne:,.0f} F",
        ])
 
    # Ligne total
    data.append([
        "", "",
        Paragraph("<b>TOTAL</b>", styles["Normal"]),
        "",
        Paragraph(f"<b>{total_general:,.0f} FCFA</b>", styles["Normal"]),
    ])
 
    col_widths = [6.5*cm, 3.5*cm, 1.5*cm, 2.8*cm, 3.2*cm]
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        # En-tête
        ("BACKGROUND",    (0, 0),  (-1, 0),  BRAND),
        ("TEXTCOLOR",     (0, 0),  (-1, 0),  colors.white),
        ("FONTNAME",      (0, 0),  (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0),  (-1, 0),  11),
        ("BOTTOMPADDING", (0, 0),  (-1, 0),  8),
        ("TOPPADDING",    (0, 0),  (-1, 0),  8),
 
        # Corps — alternance
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, GREY]),
        ("FONTSIZE",       (0, 1), (-1, -1), 10),
        ("TOPPADDING",     (0, 1), (-1, -1), 6),
        ("BOTTOMPADDING",  (0, 1), (-1, -1), 6),
 
        # Alignement colonnes numériques
        ("ALIGN",  (2, 1), (-1, -1), "CENTER"),
 
        # Ligne total
        ("BACKGROUND",  (0, -1), (-1, -1), LIGHT),
        ("FONTNAME",    (0, -1), (-1, -1), "Helvetica-Bold"),
        ("TEXTCOLOR",   (4, -1), (4, -1),  BRAND),
        ("FONTSIZE",    (4, -1), (4, -1),  12),
 
        # Bordures
        ("GRID",        (0, 0),  (-1, -1), 0.4, colors.HexColor("#CCBBAA")),
        ("LINEBELOW",   (0, 0),  (-1, 0),  1.5, BRAND),
    ]))
 
    table_width, table_height = table.wrapOn(p, width - 80, height)
    # Si le tableau dépasse la page, recule y
    if y - table_height < 60:
        p.showPage()
        y = height - 60
 
    table.drawOn(p, 40, y - table_height)
    y -= table_height + 20
 
    # ════════════════════════════════════════════════════════
    # QR CODE — lien de suivi de commande
    # ════════════════════════════════════════════════════════
    try:
        import qrcode as qr_module
        qr_data = f"https://toswe-africa.com/orders/{order.id}"
        qr_img  = qr_module.make(qr_data)
        qr_buf  = io.BytesIO()
        qr_img.save(qr_buf, format="PNG")
        qr_buf.seek(0)
 
        from reportlab.lib.utils import ImageReader
        qr_reader = ImageReader(qr_buf)
 
        qr_size = 80
        qr_x    = width - 40 - qr_size
        qr_y    = max(60, y - qr_size - 10)
 
        p.setFillColor(LIGHT)
        p.roundRect(qr_x - 8, qr_y - 8, qr_size + 16, qr_size + 30, 6, fill=1, stroke=0)
        p.drawImage(qr_reader, qr_x, qr_y, width=qr_size, height=qr_size)
        p.setFillColor(BRAND)
        p.setFont("Helvetica", 7)
        p.drawCentredString(qr_x + qr_size / 2, qr_y - 4, "Suivre ma commande")
    except Exception:
        pass  # QR code optionnel
 
    # ════════════════════════════════════════════════════════
    # FOOTER
    # ════════════════════════════════════════════════════════
    footer_y = 45
    p.setFillColor(BRAND)
    p.rect(0, 0, width, footer_y, fill=1, stroke=0)
 
    p.setFillColor(colors.white)
    p.setFont("Helvetica-Bold", 10)
    p.drawCentredString(width / 2, footer_y - 16,
                        "Merci pour votre commande chez Tôswè Africa ❤️")
    p.setFont("Helvetica", 8)
    p.drawCentredString(width / 2, footer_y - 30,
                        "toswe-africa.com  ·  Support : support@toswe-africa.com")
 
    p.showPage()
    p.save()
    buffer.seek(0)
    return ContentFile(buffer.read(), name=f"order_{order.id}.pdf")



from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_email(subject: str, message: str, recipient: str, from_email=None, is_html=True):
    """
    Envoie un email via Gmail.
    - subject : sujet du mail
    - message : contenu (peut être texte ou HTML)
    - recipient : destinataire
    - is_html : si True, envoie le message comme HTML + fallback texte
    """
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL

    try:
        # Si c'est du HTML, on génère une version texte brute simple
        if is_html:
            text_message = "Ce message contient du contenu en HTML. Veuillez utiliser un client mail compatible."
        else:
            text_message = message  # message déjà en texte brut

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_message,  # fallback texte
            from_email=from_email,
            to=[recipient],
        )

        # Si c’est du HTML → attacher la version HTML
        if is_html:
            email.attach_alternative(message, "text/html")

        email.send()
        return {"status": "success", "message": "Email envoyé ✅"}
    except Exception as e:
        return {"status": "error", "message": str(e)}




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
