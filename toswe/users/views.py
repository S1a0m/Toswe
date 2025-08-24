from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
import requests
from rest_framework.views import APIView

from users.models import CustomUser, Feedback, Notification
from products.models import Product, Cart, Order, Delivery, Payment
from .serializers import *
from toswe.payments import PaymentGateway
from toswe.utils import verify_token

from toswe.utils import send_sms

from toswe.permissions import IsUserAuthenticated


import jwt
import random
from datetime import datetime, timedelta

from django.conf import settings
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import CustomUser, SellerProfile
from .serializers import UserConnexionSerializer
from .authentication import JWTAuthentication



class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserConnexionSerializer
    authentication_classes = [JWTAuthentication]

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def init_connexion(self, request):
        """Étape 1: envoi du numéro → envoi OTP par SMS"""

        phone = request.data.get("phone")
        if not phone:
            return Response({"detail": "Numéro de téléphone requis."}, status=400)

        # Générer OTP 6 chiffres
        otp = str(random.randint(100000, 999999))

        try:
            user = CustomUser.objects.get(
                phone=phone)  # utilisateur existant → on met à jour OTP
            user.session_mdp = otp
            user.mdp_timeout = timezone.now() + timedelta(minutes=5)
            user.save()
        except CustomUser.DoesNotExist:
            # Si l'utilisateur n’existe pas → le créer (flux inscription implicite)
            user = CustomUser.objects.create(
                phone=phone, session_mdp=otp,
                mdp_timeout=timezone.now() + timedelta(minutes=5)
            )

        # Envoi SMS
        print(phone, f"Votre code de connexion Toswe est {otp}")
        return Response({"detail": "Un code temporaire a été envoyé par SMS."})

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def confirm_connexion(self, request):
        phone = request.data.get("phone")
        otp = request.data.get("session_mdp")

        if not phone or not otp:
            return Response({"detail": "Numéro de téléphone et OTP requis."}, status=400)

        try:
            user = CustomUser.objects.get(phone=phone)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Utilisateur inconnu."}, status=404)

        if user.session_mdp == otp and user.mdp_timeout > timezone.now():
            access_payload = {
                "phone": user.phone,
                "exp": datetime.utcnow() + timedelta(minutes=15)
            }
            refresh_payload = {
                "phone": user.phone,
                "type": "refresh",
                "exp": datetime.utcnow() + timedelta(days=7)
            }

            access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm="HS256")
            refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm="HS256")

            user.last_authenticated = timezone.now()
            user.save()

            is_premium = False
            is_brand = False
            if user.is_seller and hasattr(user, "seller_profile"):
                is_brand = user.seller_profile.is_brand

            if user.is_seller and hasattr(user, "seller_profile"):
                is_premium = user.seller_profile.is_premium

            response = Response({
                "access": access_token,
               # "refresh": refresh_token,
                "user": {
                    "id": user.id,
                    "phone": user.phone,
                    "is_seller": user.is_seller,
                    "is_premium": is_premium,
                    "is_brand": is_brand,
                }
            })

            response.set_cookie(
                key='refresh_token',
                value=str(refresh_token),
                httponly=True,
                secure=False,  # A securiser apres
                samesite='Lax',
                path='/',
                max_age=7 * 24 * 60 * 60  # 7 jours
             )

            return response

        else:
            return Response({"detail": "Code incorrect ou expiré."}, status=401)

    @action(detail=False, methods=["post"], url_path="logout")
    def logout(self, request):
        response = Response({"detail": "Déconnecté avec succès."}, status=status.HTTP_200_OK)

        # Supprimer le cookie contenant le refresh token
        response.delete_cookie(
            key="refresh_token",
            path="/",  # doit correspondre à celui utilisé dans set_cookie
            samesite="Lax"
        )

        return response

    @action(detail=False, methods=["get"])
    def me(self, request):
        print("Le type ce salo", type(request.user))
        user = request.user
        return Response({
            "id": user.id,
            "phone": user.phone,
            "is_seller": user.is_seller,
        })

    @action(detail=True, methods=['post'])
    def become_seller(self, request, pk=None):
        """Devenir vendeur sur Toswe (vérification via Racine)"""
        user = self.get_object()

        # Appel à l’API Racine (à adapter à ton URL réelle)
        url = "https://api.racine.bj/user-info/"
        headers = {"Authorization": f"Bearer {request.headers.get('Authorization')}"}
        payload = {"racine_id": user.racine_id}

        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code != 200:
                return Response({"detail": "Impossible de contacter Racine."}, status=502)

            data = response.json()

            # Vérifie les données obligatoires
            if not data.get("is_verified"):
                return Response({"detail": "Votre identité Racine n'est pas encore vérifiée."}, status=403)
            if not data.get("address") or not data.get("full_name"):
                return Response({"detail": "Adresse et nom complet requis via Racine."}, status=400)

            # Tu peux aussi sauvegarder ces infos localement si tu veux
            user.is_seller = True
            user.save()
            return Response({'status': 'seller enabled'})

        except Exception as e:
            return Response({"detail": "Erreur lors de la vérification Racine.", "error": str(e)}, status=500)

    @action(detail=True, methods=['post'])
    def become_premium(self, request, pk=None):
        """Seuls les vendeurs peuvent devenir premium après paiement"""
        user = self.get_object()
        payment_method = request.data.get("payment_method")  # "Moov" ou "MTN"
        user_number = request.data.get("user_number")

        if not user.is_seller:
            return Response({'status': 'Vous n\'êtes pas un vendeur.'}, status=401)

        if not payment_method or not user_number:
            return Response({'status': 'Informations incomplètes'}, status=400)

        amount = 1000  # montant du premium (par exemple)

        # Simulation de paiement
        if payment_method.lower() == "moov":
            success = PaymentGateway.pay_with_moov(user_number, amount)
        elif payment_method.lower() == "mtn":
            success = PaymentGateway.pay_with_mtn(user_number, amount)
        else:
            return Response({'status': 'Méthode de paiement invalide'}, status=400)

        if not success:
            return Response({'status': 'Échec du paiement'}, status=402)

        # Paiement réussi
        user.is_premium = True
        user.save()
        return Response({'status': 'Vendeur premium activé avec succès !'})


    @action(detail=True, methods=['get'])
    def seller_stats(self, request, pk=None):
        user = self.get_object()
        if not user.is_seller:
            return Response({'status': 'vendeur non reconnu'}, status=401)
        serializer = SellerStatisticsSerializer(user)
        return Response(serializer.data)


class RefreshTokenView(APIView):

    # @csrf_exempt
    def post(self, request):
        # Récupérer le refresh token depuis le cookie
        token = request.COOKIES.get("refresh_token")
        print("Regarde bro:", token)
        if not token:
            return Response({"detail": "Aucun refresh token trouvé."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            if payload.get("type") != "refresh":
                return Response({"detail": "Mauvais type de token."}, status=status.HTTP_401_UNAUTHORIZED)

            # Générer un nouveau access token
            new_access_payload = {
                "phone": payload["phone"],
                "exp": datetime.utcnow() + timedelta(minutes=15)
            }
            new_access_token = jwt.encode(new_access_payload, settings.SECRET_KEY, algorithm="HS256")

            return Response({"access": new_access_token})

        except jwt.ExpiredSignatureError:
            return Response({"detail": "Refresh token expiré."}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({"detail": "Token invalide."}, status=status.HTTP_401_UNAUTHORIZED)



class BrandViewSet(viewsets.ModelViewSet):
    queryset = SellerProfile.objects.filter(is_brand=True)
    serializer_class = BrandSerializer

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = UserFeedbackSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsUserAuthenticated()]
        return [AllowAny()]


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = UserNotificationsSerializer
    permission_classes = [IsUserAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Notification.objects.filter(is_deleted=False, user=user)
        return Notification.objects.none()

    def destroy(self, request, *args, **kwargs):
        """Ne supprime pas réellement la notification, mais la marque comme supprimée"""
        notification = self.get_object()
        notification.is_deleted = True
        notification.save()
        return Response({"detail": "Notification supprimée (virtuellement)."})

