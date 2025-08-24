from django.core import signing
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action

from users.models import CustomUser, UserInteractionEvent, Feedback, Notification
from products.models import Product, Cart, Order, Delivery, Payment
from users.serializers import *

from products.serializers import *

from toswe.permissions import IsUserAuthenticated

from toswe.utils import track_user_interaction
from users.authentication import JWTAuthentication

from django.core.files.uploadedfile import InMemoryUploadedFile
from .spbi_model import predict_top_k


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductDetailsSerializer
    authentication_classes = [JWTAuthentication]

    # def get_permissions(self):
    #     if self.action in ['create', 'destroy', 'update']:
    #         return [IsUserAuthenticated()]
    #     return None

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
        user = request.user
        if not user.is_authenticated:
            return Response({"detail": "Authentification requise."}, status=401)

        # Étape 1 : On regarde dans quelles catégories l'utilisateur interagit le plus
        top_categories = (
            UserInteractionEvent.objects
            .filter(user=user, product__category__isnull=False)
            .values('product__category')
            .annotate(freq=Count('id'))
            .order_by('-freq')
            .values_list('product__category', flat=True)[:3]
        )

        # Étape 2 : On récupère des produits sponsorisés dans ces catégories
        products = (
            Product.objects
            .filter(is_sponsored=True, category__in=top_categories)
            .distinct()[:10]
        )

        # Fallback : si aucune interaction, proposer des produits sponsorisés génériques
        if not products.exists():
            products = Product.objects.filter(is_sponsored=True)[:10]

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])# , url_path='qr-code')
    def get_qr_code(self, request, pk=None):
        """Retourne uniquement l'URL du QR code du produit"""
        try:
            product = self.get_object()
            if product.qr_code:
                return Response({
                    "product_id": product.id,
                    "qr_code_url": request.build_absolute_uri(product.qr_code.url)
                }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"detail": "Aucun QR code disponible pour ce produit."},
                    status=status.HTTP_404_NOT_FOUND
                )
        except Product.DoesNotExist:
            return Response(
                {"detail": "Produit introuvable."},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['get']) # , url_path='scan/(?P<signed_id>[^/.]+)', permission_classes=[AllowAny])
    def scan_product(self, request, signed_id=None):
        try:
            product_id = signing.loads(signed_id)
            product = Product.objects.get(id=product_id)
            serializer = self.get_serializer(product)
            return Response(serializer.data)
        except signing.BadSignature:
            return Response({"error": "QR code invalide"}, status=400)
        except Product.DoesNotExist:
            return Response({"error": "Produit introuvable"}, status=404)

    @action(detail=True, methods=['get'])
    def view(self, request, pk=None):
        product = self.get_object()

        # Enregistre l'interaction
        track_user_interaction(
            user=request.user,
            product=product,
            action='view'
        )

        serializer = self.get_serializer(product)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def qr_code(self, request, pk=None):
        product = self.get_object()
        pass

    @action(detail=False, methods=['get'])
    def announcements(self, request):
        products = Product.objects.filter(announcement_text__isnull=False)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post']) # , url_path='sponsor')
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

    @action(detail=False, methods=['post'], url_path='identify')
    def identify_product(self, request):
        """
        Receives an image and returns the top-k matching products with scores.
        """
        uploaded_image = request.FILES.get('image')

        if not uploaded_image:
            return Response({"error": "No image uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                for chunk in uploaded_image.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name

            # Predict top-k product IDs
            top_k_results = predict_top_k(tmp_path, k=5)  # [(id, score), ...]

            if not top_k_results:
                return Response({"error": "No prediction."}, status=status.HTTP_404_NOT_FOUND)

            # Retrieve products
            product_ids = [pid for pid, _ in top_k_results]
            products = {p.id: p for p in Product.objects.filter(id__in=product_ids)}

            # Build response list
            results = []
            for pid, score in top_k_results:
                product = products.get(pid)
                if not product:
                    continue
                results.append({
                    "id": product.id,
                    "name": product.name,
                    "main_image": request.build_absolute_uri(product.main_image.url) if product.main_image else None,
                    "price": str(product.price),
                    "short_description": product.short_description or "",
                    "score": round(score, 4),  # probabilité arrondie
                })

            return Response({"results": results}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'])
    def search_products(self, request):
        query = request.query_params.get("q", "").strip()
        if not query:
            return Response(
                {"error": "Veuillez fournir un nom de produit (paramètre ?q=)."},
                status=status.HTTP_400_BAD_REQUEST
            )

        products = Product.objects.filter(
            name__icontains=query
        ).select_related("seller__user").prefetch_related("images")

        serializer = ProductSearchSerializer(
            products, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = UserCartSerializer
    permission_classes = [IsUserAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = UserOrdersSerializer
    permission_classes = [IsUserAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["post"])
    def checkout(self, request):
        """
        Étape de paiement avant la commande.
        L'utilisateur choisit un mode de paiement : 'momo' ou 'physique'
        """
        user = request.user
        payment_method = request.data.get("payment_method")  # 'momo' ou 'physique'

        if payment_method not in ['momo', 'physique']:
            return Response({"error": "Mode de paiement invalide."}, status=400)

        cart_items = Cart.objects.filter(user=user)
        if not cart_items.exists():
            return Response({"error": "Votre panier est vide."}, status=400)

        total_amount = sum(item.product.price * item.quantity for item in cart_items)

        # Exemple de traitement momo (à implémenter réellement plus tard)
        if payment_method == "momo":
            phone = request.data.get("phone")
            if not phone:
                return Response({"error": "Numéro requis pour Mobile Money."}, status=400)
            # Appel API de paiement ici
            # if paiement_reussi:
            #     pass
            # else:
            #     return Response(...)

        # Création de la commande
        order = Order.objects.create(user=user, total_price=total_amount, payment_method=payment_method)
        for item in cart_items:
            order.items.create(product=item.product, quantity=item.quantity)
        cart_items.delete()

        return Response({"message": "Commande validée avec succès", "order_id": order.id}, status=201)

class DeliveryViewSet(viewsets.ModelViewSet):
    serializer_class = UserDeliveriesSerializer
    permission_classes = [IsUserAuthenticated]

    def get_queryset(self):
        return Delivery.objects.filter(order__user=self.request.user)



class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = UserPaymentSerializer

# class SponsoredProductViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Product.objects.filter(is_sponsored=True)
#     serializer_class = SponsoredProductsSerializer