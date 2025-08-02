from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
import requests
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
import jwt

from users.models import User, Product, Cart, Feedback, Notification, Order, Delivery, Payment
from .serializers import *


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = UserFeedbackSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = UserNotificationsSerializer

RACINE_API_URL = "https://racine.example.com/api"
RACINE_TOKEN = "your_racine_api_token"

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserConnexionSerializer

    @action(detail=False, methods=["post"])
    def init_connexion(self, request):
        """Étape 1: Soumission de l'id_racine"""
        racine_id = request.data.get("racine_id")
        try:
            user = User.objects.get(racine_id=racine_id)
            # Notifie Racine d’une tentative de connexion
            response = requests.post(f"{RACINE_API_URL}/notify-login/", json={
                "racine_id": racine_id,
                "client": "toswe"
            }, headers={"Authorization": f"Bearer {RACINE_TOKEN}"})
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
            if user.session_mdp == mdp:
                # Génère le token JWT
                payload = {
                    "user_id": user.id,
                    "racine_id": racine_id,
                    "exp": datetime.utcnow() + timedelta(days=7)
                }
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                return Response({"token": token})
            return Response({"detail": "Mot de passe incorrect."}, status=401)
        except User.DoesNotExist:
            return Response({"detail": "Utilisateur non reconnu."}, status=404)

    @action(detail=True, methods=['post'])
    def become_seller(self, request, pk=None):
        """Devenir vendeur sur Toswe"""
        user = self.get_object()
        user.is_seller = True
        user.save()
        return Response({'status': 'seller enabled'})

    @action(detail=True, methods=['post'])
    def become_premium(self, request, pk=None):
        """Seul les vendeurs peuvent devenir premium"""
        user = self.get_object()
        if not user.is_seller:
            return Response({'status': 'premium vendeur non reconnue.'}, status=401)
        user.is_premium = True
        user.save()
        return Response({'status': 'premium enabled'})

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        user = self.get_object()
        if not user.is_seller:
            return Response({'status': 'premium vendeur non reconnu'}, status=401)
        serializer = SellerStatisticsSerializer(user)
        return Response(serializer.data)


class SponsoredProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_sponsored=True)
    serializer_class = SponsoredProductsSerializer

