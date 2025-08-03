from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
import requests
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
import jwt
from rest_framework.views import APIView

from users.models import User, Product, Cart, Feedback, Notification, Order, Delivery, Payment
from .serializers import *
from ..toswe.payments import PaymentGateway
from ..toswe.permissions import IsUserAuthenticated
from ..toswe.utils import verify_token

RACINE_API_URL = "https://racine.example.com/api"
RACINE_TOKEN = "your_racine_api_token"

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserConnexionSerializer

    def get_permissions(self):
        if self.action in ['become_seller', 'become_premium', 'seller_stats']:
            return [IsUserAuthenticated]
        return [AllowAny]

    @action(detail=False, methods=["post"])
    def init_connexion(self, request):
        """Étape 1: Soumission de l'id_racine"""
        racine_id = request.data.get("racine_id")
        try:
            user = User.objects.get(racine_id=racine_id)
            # Notifie Racine d’une tentative de connexion
            response = requests.post(f"{RACINE_API_URL}/notify-login/", json={ # Racine repond avec un hash de mdp
                "racine_id": racine_id,
                "client": "toswe"
            }, headers={"Authorization": f"Bearer {RACINE_TOKEN}"})
            user.session_mdp = response.json()["session_mdp"]
            user.mdp_timeout = response.json()["mdp_timeout"]
            user.save()

            return Response({"detail": "Connexion notifiée. Veuillez confirmer sur Racine."})
        except User.DoesNotExist:
            # Vérifie existence côté Racine
            response = requests.get(f"{RACINE_API_URL}/check-user/{racine_id}/", headers={
                "Authorization": f"Bearer {RACINE_TOKEN}"
            })
            if response.status_code == 404:
                return Response({"detail": "Racine_id introuvable. Créez un compte sur Racine."}, status=404)
            elif response.status_code == 200:
                return Response({
                    "detail": "Utilisateur trouvé sur Racine. Veuillez confirmer l'inscription dans Racine et autoriser Toswe à accéder à vos données."
                })
            else:
                return Response({"detail": "Erreur côté Racine."}, status=502)

    @action(detail=False, methods=["post"])
    def confirm_connexion(self, request):
        """Étape 2: Authentification avec mot de passe temporaire"""
        racine_id = request.data.get("racine_id")
        mdp = request.data.get("session_mdp")

        try:
            user = User.objects.get(racine_id=racine_id)
            if user.session_mdp == mdp and user.mdp_timeout > timezone.now():
                # Génère le token JWT
                payload = {
                    "racine_id": racine_id,
                    "session_mdp": mdp,
                    "exp": datetime.utcnow() + timedelta(days=7)
                }
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                user.is_authenticated = True
                user.last_authenticated = timezone.now()
                user.save()

                return Response({"token": token})
            return Response({"detail": "Mot de passe incorrect ou session expirée."}, status=401)
        except User.DoesNotExist:
            return Response({"detail": "Utilisateur non reconnu."}, status=404)

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
    def post(self, request):
        user_authenticated = verify_token(request.data.get("token"))
        if user_authenticated["authenticated"]:

            # Génère un nouveau token
            payload = {
                "racine_id": user_authenticated["racine_id"],
                "session_mdp": user_authenticated["session_mdp"],
                "exp": datetime.utcnow() + timedelta(minutes=15),
            }
            new_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

            return Response({"token": new_token}, status=200)
        return Response({"detail": "Token invalide."}, status=401)


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
        return Notification.objects.filter(is_deleted=False, user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """Ne supprime pas réellement la notification, mais la marque comme supprimée"""
        notification = self.get_object()
        notification.is_deleted = True
        notification.save()
        return Response({"detail": "Notification supprimée (virtuellement)."})

