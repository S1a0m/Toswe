import jwt

from toswe.toswe import settings
from toswe.users.models import User


def verify_token(token):
    try:
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return {"authenticated": True, "detail": decoded}

    except jwt.ExpiredSignatureError:
        try:
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'], options={"verify_exp": False})
            user_id = decoded.get("user_id")
            user = User.objects.filter(id=user_id).first()
            if user:
                user.is_authenticated = False
                user.save()
        except Exception:
            pass
        return {"authenticated": False, "detail": "Token expiré"}

    except jwt.InvalidTokenError:
        return {"authenticated": False, "detail": "Token invalide"}


def is_eligible_to_be_seller(user):
    return (
        user.is_authenticated and
        user.phone_number and
        user.address
    )
