import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions

User = get_user_model()

class JWTAuthentication(authentication.BaseAuthentication):
    """
    Authentifie l'utilisateur via le JWT envoyé dans l'en-tête Authorization
    """
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None  # pas d'authentification fournie

        try:
            prefix, token = auth_header.split(" ")
            if prefix.lower() != "bearer":
                raise exceptions.AuthenticationFailed("Format d'Authorization invalide")
        except ValueError:
            raise exceptions.AuthenticationFailed("Format d'Authorization invalide")

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("Token expiré")
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed("Token invalide")

        phone = payload.get("phone")
        if not phone:
            raise exceptions.AuthenticationFailed("Token invalide : aucun phone trouvé")

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("Utilisateur introuvable")

        return (user, None)
