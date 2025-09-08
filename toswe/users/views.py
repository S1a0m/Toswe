from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
import requests
from django.db import models
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from users.models import CustomUser, Notification, UserInteractionEvent
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
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import CustomUser, SellerProfile
from .serializers import UserConnexionSerializer
from .authentication import JWTAuthentication


# parser_classes = [MultiPartParser, FormParser]

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserConnexionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

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
            is_verified = False
            slogan = ""
            about = ""
            shop_name = ""
            if user.is_seller and hasattr(user, "seller_profile"):
                is_brand = user.seller_profile.is_brand
                is_premium = user.seller_profile.is_premium
                is_verified = user.seller_profile.is_verified
                slogan = user.seller_profile.slogan
                about = user.seller_profile.about
                shop_name = user.seller_profile.shop_name

            response = Response({
                "access": access_token,
               # "refresh": refresh_token,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "address": user.address,
                    "phone": user.phone,
                    "is_seller": user.is_seller,
                    "is_premium": is_premium,
                    "is_brand": is_brand,
                    "is_verified": is_verified,
                    "shop_name": shop_name,
                    "slogan": slogan,
                    "about": about,
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
        user = request.user

        is_premium = False
        is_brand = False
        is_verified = False
        slogan = ""
        about = ""
        shop_name = ""
        if user.is_seller and hasattr(user, "seller_profile"):
            is_brand = user.seller_profile.is_brand
            is_premium = user.seller_profile.is_premium
            is_verified = user.seller_profile.is_verified
            slogan = user.seller_profile.slogan
            about = user.seller_profile.about
            shop_name = user.seller_profile.shop_name

        return Response({"id": user.id, "username": user.username, "address": user.address, "phone": user.phone,
                     "is_seller": user.is_seller, "is_premium": is_premium, "is_brand": is_brand,
                     "is_verified": is_verified, "shop_name": shop_name, "slogan": slogan, "about": about, })

    @action(detail=False, methods=["post"])
    def update_me(self, request):
        user = request.user
        data = request.data

        # Champs de base utilisateur
        username = data.get("username")
        address = data.get("address")
        phone = data.get("phone")

        if username:
            user.username = username
        if address:
            user.address = address
        if phone:
            user.phone = phone

        # Valeurs par défaut
        is_premium = False
        is_brand = False
        is_verified = False
        shop_name = ""
        slogan = ""
        about = ""

        seller_profile = None
        if user.is_seller and hasattr(user, "seller_profile"):
            seller_profile = user.seller_profile
            shop_name = data.get("shop_name", seller_profile.shop_name)
            slogan = data.get("slogan", seller_profile.slogan)
            about = data.get("about", seller_profile.about)

            seller_profile.shop_name = shop_name
            seller_profile.slogan = slogan
            seller_profile.about = about

            is_brand = seller_profile.is_brand
            is_premium = seller_profile.is_premium
            is_verified = seller_profile.is_verified

            seller_profile.save()

        user.save()

        return Response(
            {
                "id": user.id,
                "username": user.username,
                "address": user.address,
                "phone": user.phone,
                "is_seller": user.is_seller,
                "is_premium": is_premium,
                "is_brand": is_brand,
                "is_verified": is_verified,
                "shop_name": shop_name,
                "slogan": slogan,
                "about": about,

        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def interaction_events(self, request):
        events = request.data.get("events", [])
        for ev in events:
            UserInteractionEvent.objects.create(
                user=request.user,
                product_id=ev.get("product"),
                action=ev["action"],
                timestamp=ev["timestamp"],
                details=ev.get("details", {})
            )
        return Response({"status": "ok"}, status=201)

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def sellers(self, request):
        """
        Récupère la liste des vendeurs.
        Les vendeurs premium apparaissent en premier,
        suivis des marques, puis des vendeurs classiques.
        """
        sellers = SellerProfile.objects.all()

        # Tri personnalisé
        sellers = sellers.order_by(
            # Premium en premier
            models.Case(
                models.When(is_premium=True, then=0),
                models.When(is_brand=True, then=1),
                default=2,
                output_field=models.IntegerField(),
            )
        )

        serializer = SellerListSerializer(sellers, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def brands(self, request):
        """
        Retourner toutes les marques (SellerProfile),
        d'abord premium puis non premium.
        """
        # Récupérer tous les profils vendeur
        sellers = SellerProfile.objects.all().order_by("-is_premium", "shop_name")

        serializer = BrandSerializer(sellers, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="verify_account")
    def verify_account(self, request):
        user = request.user

        # if not user.is_authenticated:
        #     return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_seller:
            return Response({"error": "Only sellers can verify their account"}, status=status.HTTP_403_FORBIDDEN)

        seller_profile = getattr(user, "seller_profile", None)
        if not seller_profile:
            return Response({"error": "Seller profile not found"}, status=status.HTTP_404_NOT_FOUND)

        id_card = request.FILES.get("id_card")
        commercial_register = request.FILES.get("commercial_register")

        if not id_card or not commercial_register:
            return Response(
                {"error": "Both ID card and commercial register are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Sauvegarde des fichiers
        seller_profile.id_card = id_card
        seller_profile.commercial_register = commercial_register
        seller_profile.is_verified = False  # toujours false → admin doit confirmer
        seller_profile.save()

        return Response({
            "message": "Documents uploaded successfully. Verification pending.",
            "is_verified": seller_profile.is_verified
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"])
    def become_seller(self, request):
        serializer = BecomeSellerSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        return Response({
            "message": "Votre profil vendeur a été créé/mis à jour avec succès.",
            "seller_profile": BecomeSellerSerializer(profile).data
        }, status=status.HTTP_201_CREATED)

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



class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = UserNotificationsSerializer
    authentication_classes = [JWTAuthentication]

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

