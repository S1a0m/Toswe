from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from users.models import User, Product, Cart, Feedback, Notification, Order, Delivery, Payment
from users.serializers import *

from toswe.users.serializers import *


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductDetailsSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailsSerializer
        elif self.action == 'suggestions':
            return ProductSuggestionsSerializer
        elif self.action == 'announcements':
            return AnnouncementsProductsSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=['get'])
    def suggestions(self, request):
        products = Product.objects.filter(is_sponsored=True)[:10]
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def announcements(self, request):
        products = Product.objects.filter(announcement_text__isnull=False)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='sponsor')
    def sponsor_product(self, request, pk=None):
        product = self.get_object()
        user = request.user

        # Vérifie que l'utilisateur est bien le vendeur du produit
        if product.seller != user:
            return Response(
                {"error": "Vous n'êtes pas autorisé à sponsoriser ce produit."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Vérifie que l'utilisateur a un compte premium
        if not user.is_premium:
            return Response(
                {"error": "Seuls les vendeurs premium peuvent sponsoriser des produits."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Vérifie s'il a déjà atteint la limite de produits sponsorisés
        sponsored_count = Product.objects.filter(seller=user, is_sponsored=True).count()
        MAX_SPONSORED = 5

        if sponsored_count >= MAX_SPONSORED:
            return Response(
                {"error": f"Limite atteinte : vous avez déjà {MAX_SPONSORED} produits sponsorisés."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Vérifie si le produit est déjà sponsorisé
        if product.is_sponsored:
            return Response(
                {"message": "Ce produit est déjà sponsorisé."},
                status=status.HTTP_200_OK
            )

        # Sponsorise le produit
        product.is_sponsored = True
        product.save()

        return Response(
            {"message": "Produit sponsorisé avec succès."},
            status=status.HTTP_200_OK
        )


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = UserCartSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = UserOrdersSerializer


class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = UserDeliveriesSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = UserPaymentSerializer

class SponsoredProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_sponsored=True)
    serializer_class = SponsoredProductsSerializer