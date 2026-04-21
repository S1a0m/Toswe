from django.db.models import Sum, F, When, Case, IntegerField
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
import requests
from django.db import models
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser

from users.models import CustomUser, Notification, UserInteractionEvent
from products.models import Product, Cart, Order, Delivery, Payment, OrderItem
from .serializers import *
from toswe.payments import PaymentGateway
from toswe.utils import verify_token

from toswe.utils import send_email

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

from rest_framework.decorators import api_view
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserConnexionSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def init_connexion(self, request):
        """Étape 1: envoi du numéro → envoi OTP par SMS"""

        email = request.data.get("email")
        is_subscriber = False
        if not email:
            return Response({"detail": "Email requis."}, status=400)

        # Générer OTP 6 chiffres
        otp = str(random.randint(100000, 999999))

        try:
            user = CustomUser.objects.get(
                email=email)  # utilisateur existant → on met à jour OTP
            user.session_mdp = otp
            user.mdp_timeout = timezone.now() + timedelta(minutes=5)
            user.save()
            is_subscriber = True
        except CustomUser.DoesNotExist:
            # Si l'utilisateur n’existe pas → le créer (flux inscription implicite)
            user = CustomUser.objects.create(
                email=email, session_mdp=otp,
                mdp_timeout=timezone.now() + timedelta(minutes=5)
            )
            is_subscriber = False

        # Envoi SMS
        print(email, f"Votre code de connexion Tôswè est {otp}")
        send_email(
            "Connexion Tôswè",
            f"""
            <html>
            <head>
                <style>
                body {{
                    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                    background-color: #fdf8f5;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background: #ffffff;
                    border-radius: 12px;
                    overflow: hidden;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
                }}
                .header {{
                    background: linear-gradient(135deg, #7D260F, #A13B20);
                    padding: 20px;
                    text-align: center;
                    color: white;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 20px;
                    letter-spacing: 1px;
                }}
                .content {{
                    padding: 30px;
                    color: #333333;
                    line-height: 1.6;
                    font-size: 15px;
                }}
                .otp-box {{
                    display: inline-block;
                    padding: 14px 28px;
                    margin: 20px 0;
                    background: #f6d8b6;
                    color: #7D260F;
                    font-size: 24px;
                    font-weight: bold;
                    border-radius: 8px;
                    letter-spacing: 2px;
                }}
                .footer {{
                    text-align: center;
                    font-size: 12px;
                    color: #888888;
                    padding: 20px;
                }}
                </style>
            </head>
            <body>
                <div class="container">
                <div class="header">
                    <h1>Connexion à Tôswè</h1>
                </div>
                <div class="content">
                    <p>Bonjour 👋🏽,</p>
                    <p>Voici votre code de connexion à Tôswè&nbsp;:</p>
                    <div class="otp-box">{otp}</div>
                    <p>⚠️ Si vous n’êtes pas à l’origine de cette demande, vous pouvez ignorer cet email en toute sécurité.</p>
                    <p>Merci de faire confiance à <strong>Tôswè Africa</strong> pour vos emplettes locales 💛.</p>
                </div>
                <div class="footer">
                    &copy; {2025} Tôswè Africa — Tous droits réservés.<br/>
                    Ceci est un email automatique, merci de ne pas y répondre.
                </div>
                </div>
            </body>
            </html>
            """,
            email
        )

        return Response({"detail": "Un code temporaire a été envoyé par email.", "is_subscriber": is_subscriber})

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def confirm_connexion(self, request):
        email    = request.data.get("email")
        otp      = request.data.get("otp")
        username = request.data.get("username", "").strip()
        phone    = request.data.get("phone", "").strip()

        if not email or not otp:
            return Response(
                {"detail": "Email et OTP requis."},
                status=400,
            )

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Utilisateur inconnu."}, status=404)

        # ── 1. Vérifie l'OTP EN PREMIER ──────────────────────────
        # On ne touche à rien tant que le code n'est pas validé.
        if user.session_mdp != otp or user.mdp_timeout < timezone.now():
            return Response({"detail": "Code incorrect ou expiré."}, status=401)

        # ── 2. Complète le profil si nouvel utilisateur ───────────
        # Un nouvel utilisateur n'a pas encore de username.
        if not user.username:
            if not username:
                return Response(
                    {"detail": "Pseudo requis pour créer votre compte."},
                    status=400,
                )
            user.username = username
            user.phone    = phone or None   # phone optionnel à l'inscription

        # ── 3. Met à jour last_authenticated et sauvegarde ────────
        user.last_authenticated = timezone.now()
        user.save()   # ← maintenant username est garanti non-null

        # ── 4. Génère les tokens ──────────────────────────────────
        access_payload = {
            "email": user.email,
            "exp":   datetime.utcnow() + timedelta(minutes=30),
        }
        refresh_payload = {
            "email": user.email,
            "type":  "refresh",
            "exp":   datetime.utcnow() + timedelta(days=7),
        }
        access_token  = jwt.encode(access_payload,  settings.SECRET_KEY, algorithm="HS256")
        refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm="HS256")

        # ── 5. Construit les données vendeur / livreur ────────────
        is_premium   = False
        is_brand     = False
        is_verified  = False
        is_seller    = False
        is_deliverer = False
        slogan       = ""
        about        = ""
        shop_name    = ""
        logo         = None
        shop_id      = None

        if hasattr(user, "deliverer_profile") and user.deliverer_profile.is_verified:
            is_deliverer = True

        if hasattr(user, "seller_profile") and user.seller_profile.show_on_market:
            sp          = user.seller_profile
            is_seller   = True
            is_brand    = sp.is_brand
            is_premium  = sp.is_premium
            is_verified = sp.is_verified
            slogan      = sp.slogan
            about       = sp.about
            shop_name   = sp.shop_name
            shop_id     = sp.id
            logo        = sp.logo.url if sp.logo else None

        # ── 6. Retourne la réponse ────────────────────────────────
        response = Response({
            "access": access_token,
            "user": {
                "id":          user.id,
                "shop_id":     shop_id,
                "username":    user.username,
                "address":     user.address,
                "email":       user.email,
                "is_seller":   is_seller,
                "is_deliverer":is_deliverer,
                "is_premium":  is_premium,
                "is_brand":    is_brand,
                "is_verified": is_verified,
                "shop_name":   shop_name,
                "slogan":      slogan,
                "about":       about,
                "logo":        logo,
            },
        })

        # Refresh token en cookie httpOnly (plus sécurisé que dans le body)
        response.set_cookie(
            key      = "refresh_token",
            value    = str(refresh_token),
            httponly = True,
            secure   = False,   # passer à True en production (HTTPS)
            samesite = "Lax",
            path     = "/",
            max_age  = 7 * 24 * 60 * 60,   # 7 jours
        )

        return response

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
        is_seller = False
        is_deliverer = False
        slogan = ""
        about = ""
        shop_name = ""
        logo = None
        shop_id = None

        if hasattr(user, "deliverer_profile"):
            if user.deliverer_profile.is_verified:
                is_deliverer = True
        if hasattr(user, "seller_profile"):
            if user.seller_profile.show_on_market:
                is_brand = user.seller_profile.is_brand
                is_premium = user.seller_profile.is_premium
                is_verified = user.seller_profile.is_verified
                slogan = user.seller_profile.slogan
                about = user.seller_profile.about
                shop_name = user.seller_profile.shop_name
                shop_id = user.seller_profile.id
                logo = user.seller_profile.logo.url if user.seller_profile.logo else None
                is_seller = True

        return Response({"id": user.id, "shop_id": shop_id,"username": user.username, "address": user.address, "email": user.email,
                     "is_seller": is_seller, "is_deliverer": is_deliverer, "is_premium": is_premium, "is_brand": is_brand,
                     "is_verified": is_verified, "shop_name": shop_name, "slogan": slogan, "about": about, "logo": logo})

    @action(detail=False, methods=["post"])
    def update_me(self, request):
        user = request.user
        data = request.data

        # Champs de base utilisateur
        username = data.get("username")
        address = data.get("address")
        email = data.get("email")

        if username:
            user.username = username
        if address:
            user.address = address
        if email:
            user.email = email

        # Valeurs par défaut
        is_premium = False
        is_brand = False
        is_verified = False
        is_seller = False
        is_deliverer = False
        shop_name = ""
        slogan = ""
        about = ""
        logo = ""
        shop_id = None

        seller_profile = None
        if hasattr(user, "deliverer_profile"):
            if user.deliverer_profile.is_verified:
                is_deliverer = True
        if hasattr(user, "seller_profile"):
            seller_profile = user.seller_profile
            shop_name = data.get("shop_name", seller_profile.shop_name)
            slogan = data.get("slogan", seller_profile.slogan)
            about = data.get("about", seller_profile.about)

            seller_profile.shop_name = shop_name
            seller_profile.slogan = slogan
            seller_profile.about = about

            # ✅ Logo : uniquement si un fichier est envoyé
            if request.FILES.get("logo"):
                seller_profile.logo = request.FILES["logo"]

            is_brand = seller_profile.is_brand
            is_premium = seller_profile.is_premium
            is_verified = seller_profile.is_verified
            shop_id = seller_profile.id
            is_seller = True

            seller_profile.save()

            # ✅ URL propre après sauvegarde
            logo = seller_profile.logo.url if seller_profile.logo else None

        user.save()

        return Response(
            {
                "id": user.id,
                "shop_id": shop_id,
                "username": user.username,
                "address": user.address,
                "email": user.email,
                "is_seller": is_seller,
                "is_deliverer": is_deliverer,
                "is_premium": is_premium,
                "is_brand": is_brand,
                "is_verified": is_verified,
                "shop_name": shop_name,
                "slogan": slogan,
                "about": about,
                "logo": logo,

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

    @action(detail=True, methods=["get"], url_path="is-subscribed")
    def is_subscribed(self, request, pk=None):
        """Vérifie si l'utilisateur courant est abonné à ce vendeur"""
        try:
            seller_profile = SellerProfile.objects.get(id=pk)
        except SellerProfile.DoesNotExist:
            return Response({"detail": "seller not found."}, status=status.HTTP_404_NOT_FOUND)
        
        client = request.user


        subscribed = seller_profile.subscribers.filter(id=client.id).exists()
        return Response({"subscribed": subscribed})

    @action(detail=True, methods=["post"], url_path="subscribe")
    def subscribe(self, request, pk=None):
        """Toggle abonnement (abonner/désabonner) et renvoie l'état final"""
        try:
            seller_profile = SellerProfile.objects.get(id=pk)
        except SellerProfile.DoesNotExist:
            return Response({"detail": "seller not found."}, status=status.HTTP_404_NOT_FOUND)

        print("Vendeur ou client?", type(seller_profile))
        
        client = request.user

        # Toggle abonnement
        if seller_profile.subscribers.filter(id=client.id).exists():
            seller_profile.subscribers.remove(client)
            subscribed = False
        else:
            seller_profile.subscribers.add(client)
            subscribed = True

        return Response({"subscribed": subscribed})

    @action(detail=False, methods=["post"])
    def become_seller(self, request):
        serializer = BecomeSellerSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        profile = serializer.save()
        return Response({
            "message": "Votre profil vendeur a été créé/mis à jour avec succès.",
            "seller_profile": BecomeSellerSerializer(profile).data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=["delete"], url_path="delete-account")
    def delete_account(self, request):
        """Permet à l’utilisateur connecté de supprimer son propre compte"""
        user = request.user
        user.delete()

        response = Response({"detail": "Compte supprimé avec succès."}, status=204)

        # Supprimer le cookie refresh_token pour éviter réutilisation
        response.delete_cookie(
            key="refresh_token",
            path="/",
            samesite="Lax"
        )

        return response
    


class SellerProfileViewSet(viewsets.ModelViewSet):
    queryset = SellerProfile.objects.all()
    serializer_class = SellerProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = None  # désactive la pagination pour les listes de vendeurs

    @action(detail=False, methods=["get"])
    def my_stats(self, request):
        user = request.user
        if not user.is_authenticated or not hasattr(user, "seller_profile"):
            return Response({"detail": "Vous n'êtes pas un vendeur."}, status=403)

        seller = user.seller_profile

        total_products = Product.objects.filter(seller=seller, is_online=True).count()

        from django.utils.timezone import now
        from datetime import timedelta
        one_month_ago = now() - timedelta(days=30)

        agg = OrderItem.objects.filter(
            order__created_at__gte=one_month_ago,
            order__status="delivered",
            product__seller=seller
        ).aggregate(
            sales_30d=Count("quantity"),
            revenue_30d=Sum(F("quantity") * F("price"))
        )

        sales_30d = agg["sales_30d"] or 0
        revenue_30d = agg["revenue_30d"] or 0

        # ✅ loycs devient un objet JSON comme total_rating
        rating_agg = Feedback.objects.filter(
            product__seller=seller
        ).aggregate(
            avg=Avg("rating"),
            count=Count("id")
        )

        data = {
            "products_active": total_products,
            "sales_30d": sales_30d,
            "revenue_30d": revenue_30d,
            "loycs": {
                "average": round(rating_agg["avg"], 1) if rating_agg["avg"] else 0,
                "count": rating_agg["count"] or 0,
            },
        }
        return Response(data)

    @action(detail=False, methods=["get"])
    def my_subscribers(self, request):
        user = request.user
        if not user.is_authenticated or not hasattr(user, "seller_profile"):
            return Response({"detail": "Vous n’êtes pas un vendeur."}, status=403)

        seller = user.seller_profile

        subscribers = seller.subscribers.all() if hasattr(seller, "subscribers") else []

        data = []
        for sub in subscribers:
            orders_count = Order.objects.filter(
                user=sub,
                items__product__seller=seller
            ).distinct().count()
            data.append({
                "id": sub.id,
                "username": sub.username,
                "phone": sub.phone,
                "orders_count": orders_count,
            })

        return Response(data)
    
    @action(detail=False, methods=['post'])
    def become_premium(self, request):
        user = request.user
        seller_profile = getattr(user, "seller_profile", None)
        if not seller_profile:
            return Response({"error": "Seller profile not found"}, status=status.HTTP_404_NOT_FOUND)

        payment_method = request.data.get("payment_method")
        user_number = request.data.get("user_number")

        if not payment_method or not user_number:
            return Response({'status': 'Informations incomplètes'}, status=400)

        amount = 1000  # Montant premium (à ajuster)

        # Simulation de paiement
        if payment_method.lower() == "moov_money":
            success = PaymentGateway.pay_with_moov(user_number, amount)
        elif payment_method.lower() == "mtn_momo":
            success = PaymentGateway.pay_with_mtn(user_number, amount)
        else:
            return Response({'status': 'Méthode de paiement invalide'}, status=400)

        if not success:
            return Response({'status': 'Échec du paiement'}, status=402)

        # ✅ Paiement réussi → activer premium pour 30 jours
        seller_profile.is_premium = True
        seller_profile.premium_expires_at = timezone.now() + timedelta(days=30)
        seller_profile.save()

        Notification.objects.create(
            user=user,
            title="Premium",
            message="Votre compte est desormais premium. L'aventure pour vous vient de commencer."
        )

        return Response({
            'status': 'Vendeur premium activé avec succès !',
            'expires_at': seller_profile.premium_expires_at
        })
    
    @action(detail=False, methods=['post'])
    def become_brand(self, request):
        user = request.user
        seller_profile = getattr(user, "seller_profile", None)
        if not seller_profile:
            return Response({"error": "Seller profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # 🔹 Toggle (inverser la valeur)
        seller_profile.is_brand = not seller_profile.is_brand
        seller_profile.save()

        return Response({
            'seller_is_brand': seller_profile.is_brand
        }, status=status.HTTP_200_OK)
    

    @action(detail=False, methods=["post"], url_path="verify_account")
    def verify_account(self, request):
        user = request.user

        # if not user.is_authenticated:
        #     return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

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

        Notification.objects.create(
            user=user,
            title="Demande de verification de compte",
            message="Votre demande a ete bien recue. Nous vous repondrons dans quelques heures."
        )

        return Response({
            "message": "Documents uploaded successfully. Verification pending.",
            "is_verified": seller_profile.is_verified
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def sellers(self, request):
        """
        Liste complète des vendeurs (auth requis).
        Tri : Premium > Marques > Autres
        Puis par nombre d'abonnés décroissant.
        """
        sellers = (
                SellerProfile.objects.filter(show_on_market=True)
                .annotate(subscriber_count=Count("subscribers"))
                .order_by(
                    Case(
                        When(is_premium=True, then=0),
                        When(is_brand=True, then=1),
                        When(is_verified=True, then=2),
                        default=2,
                        output_field=IntegerField(),
                    ),
                    "-subscriber_count",
                )
            )
        serializer = SellerListSerializer(sellers, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Top 5 (public)
    @action(detail=False, methods=["get"], permission_classes=[AllowAny], url_path="top-sellers")
    def top_sellers(self, request):
        """
        Top 5 vendeurs (accessible à tous).
        Même tri que `sellers`, mais limité aux 5 premiers.
        """
        sellers = (
            SellerProfile.objects.filter(show_on_market=True)
            .annotate(subscriber_count=Count("subscribers"))
            .order_by(
                    Case(
                        When(is_premium=True, then=0),
                        When(is_brand=True, then=1),
                        When(is_verified=True, then=2),
                        default=2,
                        output_field=IntegerField(),
                    ),
                    "-subscriber_count",
                )[:5]
        )
        serializer = SellerListSerializer(sellers, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"], permission_classes=[AllowAny])
    def shop_header(self, request, pk=None):
        """Retourne les infos du header d'une boutique"""
        seller_profile = self.get_object()  # ← Seller

        serializer = ShopHeaderSerializer(seller_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def brands(self, request):
        """
        Retourner toutes les marques (SellerProfile),
        d'abord premium puis non premium.
        """
        # Récupérer tous les profils vendeur
        sellers = SellerProfile.objects.filter(is_brand=True, show_on_market=True).order_by("-is_premium", "shop_name")[:5]

        serializer = BrandSerializer(sellers, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class DelivererProfileViewSet(viewsets.ModelViewSet):
    queryset = DelivererProfile.objects.all()
    serializer_class = DelivererProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return DelivererProfile.objects.all()
        return DelivererProfile.objects.filter(user=user)

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Retourne le profil du livreur connecté"""
        try:
            profile = request.user.deliverer_profile
        except DelivererProfile.DoesNotExist:
            return Response({"detail": "Profil non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """Vérifier le profil du livreur (admin only)"""
        profile = self.get_object()
        profile.is_verified = True
        profile.save()
        return Response({"detail": "Profil vérifié"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def add_delivery(self, request, pk=None):
        """Ajouter un utilisateur à la liste des livraisons"""
        profile = self.get_object()
        user_id = request.data.get("user_id")
        if not user_id:
            return Response({"detail": "user_id requis"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user_to_deliver = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"detail": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        profile.deliver_to.add(user_to_deliver)
        profile.status = 'on_delivery'
        profile.save()
        return Response({"detail": "Utilisateur ajouté aux livraisons et statut mis à jour"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def complete_delivery(self, request, pk=None):
        """Marquer une livraison comme terminée et ajouter le revenu"""
        profile = self.get_object()
        user_id = request.data.get("user_id")
        amount = request.data.get("amount", 0)
        try:
            user_to_deliver = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"detail": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

        profile.deliver_to.remove(user_to_deliver)
        profile.total_income += float(amount)
        # Si plus de livraisons en cours, on remet le statut sur disponible
        if profile.deliver_to.count() == 0:
            profile.status = 'available'
        profile.save()
        return Response({"detail": "Livraison terminée et revenu mis à jour"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def set_status(self, request, pk=None):
        """Mettre à jour le statut du livreur"""
        profile = self.get_object()
        status_value = request.data.get("status")
        if status_value not in dict(DelivererProfile.STATUS_CHOICES):
            return Response({"detail": "Statut invalide"}, status=status.HTTP_400_BAD_REQUEST)
        profile.status = status_value
        profile.save()
        return Response({"detail": f"Statut mis à jour à {status_value}"}, status=status.HTTP_200_OK)


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
                "email": payload["email"],
                "exp": datetime.utcnow() + timedelta(minutes=30)
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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Notification.objects.filter(is_deleted=False, user=user).order_by("-created_at")
        return Notification.objects.none()

    # Marquer UNE notification comme lue
    @action(detail=True, methods=["post"])
    def read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({"detail": "Notification marked as read."})

    # Marquer TOUTES les notifications comme lues
    @action(detail=False, methods=["post"])
    def read_all(self, request):
        count = self.get_queryset().update(is_read=True)
        return Response({"detail": f"{count} notifications marked as read."})

    # Supprimer UNE notification (soft delete)
    @action(detail=True, methods=["delete"])
    def delete(self, request, pk=None):
        notification = self.get_object()
        notification.is_deleted = True
        notification.save()
        return Response({"detail": "Notification deleted."})

    # Supprimer TOUTES les notifications (soft delete en lot)
    @action(detail=False, methods=["delete"])
    def delete_all(self, request):
        count = self.get_queryset().update(is_deleted=True)
        return Response({"detail": f"{count} notifications deleted."})


