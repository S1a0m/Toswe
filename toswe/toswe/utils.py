import jwt

from toswe import settings
from users.models import CustomUser, UserInteractionEvent
from twilio.rest import Client
from django.conf import settings


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
