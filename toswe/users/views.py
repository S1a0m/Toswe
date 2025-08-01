from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import User, Product, Cart, Feedback, Notification, Order, Delivery, Payment
from .serializers import *


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer

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


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = UserCartSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = UserFeedbackSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = UserNotificationsSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = UserOrdersSerializer


class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = UserDeliveriesSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = UserPaymentSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserConnexionSerializer

    @action(detail=True, methods=['post'])
    def become_seller(self, request, pk=None):
        user = self.get_object()
        user.is_seller = True
        user.save()
        return Response({'status': 'seller enabled'})

    @action(detail=True, methods=['post'])
    def become_premium(self, request, pk=None):
        user = self.get_object()
        user.is_premium = True
        user.save()
        return Response({'status': 'premium enabled'})

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        user = self.get_object()
        serializer = SellerStatisticsSerializer(user)
        return Response(serializer.data)


class SponsoredProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_sponsored=True)
    serializer_class = SponsoredProductsSerializer

