from django.core import signing
from django.db.models import Q, Count, Case, When, Value, BooleanField, IntegerField, Prefetch
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from django.utils.timezone import now

from users.models import CustomUser, UserInteractionEvent, Notification, SellerProfile
from products.models import Product, Cart, Order, Delivery, Payment, CartItem, Ad, Promotion, OrderItem
from users.serializers import *

from products.serializers import *

from toswe.permissions import IsUserAuthenticated

from toswe.utils import track_user_interaction
from users.authentication import JWTAuthentication

from django.core.files.uploadedfile import InMemoryUploadedFile

from .models import Category
from .serializers import CategorySerializer, OrderListSerializer, OrderSerializer
from .spbi_model import predict_top_k


from django.utils import timezone
from datetime import timedelta

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductDetailsSerializer
    authentication_classes = [JWTAuthentication]
    #permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        """
        Définit dynamiquement les permissions selon l’action.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        elif self.action in ['list', 'retrieve']:
            return [IsAuthenticatedOrReadOnly()]
        return [AllowAny()]  # fallback explicite

    def get_serializer_class(self):
        if self.action in ['suggestions', 'similar']:
            return ProductSerializer
        elif self.action == 'retrieve':
            return ProductDetailsSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProductCreateSerializer
        elif self.action == 'announcements':
            return AnnouncementsProductsSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        # serializer.create() s'occupe du seller depuis request context, donc juste save avec context injecté automatiquement
        serializer.save()

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def suggestions(self, request):
        """
        Suggestions de produits :
        - Utilisateur connecté → boost sur ses catégories fréquentes.
        - Non connecté → suggestions génériques.
        - Supporte ?category=tout ou ?category=<slug>.
        - Mélange sponsorisés, promos, populaires, nouveaux, et fallback.
        """
        user = request.user if request.user and request.user.is_authenticated else None
        category_param = request.query_params.get("category", "tout").lower()

        # Étape 1 : Catégories prioritaires
        top_categories = []
        if user:
            top_categories = list(
                UserInteractionEvent.objects
                .filter(user=user, product__category__isnull=False)
                .values("product__category")
                .annotate(freq=Count("id"))
                .order_by("-freq")
                .values_list("product__category", flat=True)[:3]
            )

        products = Product.objects.all()

        if category_param != "tout":
            products = products.filter(category__name__iexact=category_param)

        # Étape 2 : priorisation par pub/promo/popularité
        now = timezone.now()

        sponsored_ids = Ad.objects.filter(
            ad_type="sponsored", is_active=True, ended_at__gte=now
        ).values_list("product_id", flat=True)

        promo_ids = Promotion.objects.filter(
            ended_at__gte=now
        ).values_list("product_id", flat=True)

        popular_ids = (
            CartItem.objects.values("product")
            .annotate(count=Count("id"))
            .filter(count__gte=10)
            .values_list("product", flat=True)
        )

        products = products.annotate(
            priority=(
                Case(When(category__in=top_categories, then=Value(5)), default=Value(0),
                     output_field=IntegerField()) +
                Case(When(id__in=sponsored_ids, then=Value(4)), default=Value(0),
                     output_field=IntegerField()) +
                Case(When(id__in=promo_ids, then=Value(3)), default=Value(0),
                     output_field=IntegerField()) +
                Case(When(id__in=popular_ids, then=Value(2)), default=Value(0),
                     output_field=IntegerField()) +
                Case(When(created_at__gte=now - timedelta(days=30), then=Value(1)),
                     default=Value(0), output_field=IntegerField())
            )
        ).order_by("-priority", "-created_at")

        # Étape 3 : fallback
        if not products.exists():
            products = Product.objects.all().order_by("-created_at")

        # Pagination
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def similar(self, request, pk=None):
        """
        Produits similaires :
        - Basés sur la catégorie du produit cible.
        - Priorité : sponsorisés, promos, populaires, nouveaux, puis interactions.
        """
        try:
            target_product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"detail": "Produit non trouvé."}, status=404)

        user = request.user if request.user and request.user.is_authenticated else None
        now = timezone.now()

        products = Product.objects.filter(category=target_product.category).exclude(id=target_product.id)

        sponsored_ids = Ad.objects.filter(
            ad_type="sponsored", is_active=True, ended_at__gte=now
        ).values_list("product_id", flat=True)

        promo_ids = Promotion.objects.filter(
            ended_at__gte=now
        ).values_list("product_id", flat=True)

        popular_ids = (
            CartItem.objects.values("product")
            .annotate(count=Count("id"))
            .filter(count__gte=10)
            .values_list("product", flat=True)
        )

        user_interacted = []
        if user:
            user_interacted = list(
                UserInteractionEvent.objects.filter(
                    user=user,
                    product__category=target_product.category
                ).values_list("product_id", flat=True)
            )

        products = products.annotate(
            priority=(
                Case(When(id__in=sponsored_ids, then=Value(4)), default=Value(0), output_field=IntegerField()) +
                Case(When(id__in=promo_ids, then=Value(3)), default=Value(0), output_field=IntegerField()) +
                Case(When(id__in=popular_ids, then=Value(2)), default=Value(0), output_field=IntegerField()) +
                Case(When(created_at__gte=now - timedelta(days=30), then=Value(1)),
                     default=Value(0), output_field=IntegerField()) +
                Case(When(id__in=user_interacted, then=Value(5)), default=Value(0),
                     output_field=IntegerField())
            )
        ).order_by("-priority", "-created_at").distinct()[:10]

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def seller_products(self, request, pk=None):
        """
        Retourne la liste des produits d'un vendeur donné (pk = id du seller).
        - Supporte la pagination.
        - Utilise ProductSerializer par défaut pour la liste.
        """

        try:
            seller = SellerProfile.objects.get(pk=pk)
        except SellerProfile.DoesNotExist:
            return Response({"detail": "Vendeur introuvable."}, status=status.HTTP_404_NOT_FOUND)

        products = Product.objects.filter(seller=seller).order_by("-created_at")

        # Pagination
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

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

class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all().select_related("product", "product__seller")
    serializer_class = PromotionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        """
        Lorsqu’un vendeur crée une promotion, on s’assure que
        la promotion est liée à son produit.
        """
        product = serializer.validated_data["product"]
        # Vérifie que l’utilisateur connecté est bien le vendeur du produit
        if hasattr(product, "seller") and product.seller.user == self.request.user:
            serializer.save()
        #else:
            #raise serializers.ValidationError("Vous ne pouvez créer une promotion que pour vos propres produits.")

    @action(detail=False, methods=["get"], url_path="seller/(?P<seller_id>[^/.]+)")
    def by_seller(self, request, seller_id=None):
        """
        Retourne toutes les promotions d’un vendeur spécifique.
        - Les clients voient uniquement les promotions actives
        - Le vendeur lui-même voit toutes ses promotions
        """
        qs = self.get_queryset().filter(product__seller__id=seller_id)

        # Si ce n’est pas le vendeur connecté → filtrer sur les promos actives
        if request.user.is_authenticated:
            if not qs.filter(product__seller__user=request.user).exists():
                qs = qs.filter(ended_at__gte=now())
        else:
            qs = qs.filter(ended_at__gte=now())

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class AdViewSet(viewsets.ModelViewSet):
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Ad.objects.select_related("product", "product__seller", "seller")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(is_active=True, ad_type="generic")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user
        seller = getattr(user, "seller_profile", None)
        if not seller:
            raise PermissionDenied("Seuls les vendeurs peuvent créer une publicité.")
        serializer.save(seller=seller)

    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def by_seller(self, request):
        """
        Retourne uniquement les pubs "generic" en cours du vendeur connecté.
        """
        seller = getattr(request.user, "seller_profile", None)
        if not seller:
            return Response([], status=200)  # pas vendeur → pas de pubs

        qs = self.get_queryset().filter(
            seller=seller,
            ended_at__gte=now()
        )
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 🔒 filtre par utilisateur
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def me(self, request):
        """
        Récupérer le panier de l’utilisateur connecté
        """
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def sync(self, request):
        """
        ⚡ Remplace entièrement le panier de l’utilisateur connecté
        (le frontend pousse son localStorage → serveur)
        """
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ["list", "as_seller"]:
            return OrderListSerializer
        elif self.action == "retrieve":
            return OrderSerializer
        else:
            return OrderSerializer

    def get_queryset(self):
        """
        Par défaut → commandes du client connecté.
        """
        if self.request.user.is_authenticated:
            return Order.objects.filter(user=self.request.user).prefetch_related("items__product")
        return Order.objects.none()

    def retrieve(self, request, *args, **kwargs):
        """
        Permet à :
        - l’acheteur de voir sa commande
        - le vendeur des produits inclus de voir la commande
        """
        instance = get_object_or_404(Order, pk=kwargs["pk"])

        user = request.user
        if instance.user == user:
            # cas acheteur
            pass
        elif user.is_seller and hasattr(user, "seller_profile"):
            # cas vendeur
            seller_profile = user.seller_profile
            if not instance.items.filter(product__seller=seller_profile).exists():
                return Response({"detail": "Vous n’avez pas accès à cette commande."}, status=403)
        else:
            return Response({"detail": "Vous n’avez pas accès à cette commande."}, status=403)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def as_seller(self, request):
        """
        Liste toutes les commandes contenant au moins un produit du vendeur connecté.
        """
        user = request.user
        if not user.is_authenticated or not user.is_seller:
            return Response({"detail": "Accès réservé aux vendeurs."}, status=403)

        seller_profile = getattr(user, "seller_profile", None)
        if not seller_profile:
            return Response({"detail": "Pas de profil vendeur trouvé."}, status=404)

        qs = Order.objects.filter(
            items__product__seller=seller_profile
        ).prefetch_related(
            Prefetch("items", queryset=OrderItem.objects.select_related("product"))
        ).distinct()

        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)



class DeliveryViewSet(viewsets.ModelViewSet):
    serializer_class = DeliveriesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Delivery.objects.filter(order__user=self.request.user)

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all().order_by("-created_at")
    serializer_class = FeedbackSerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Lorsqu'un utilisateur crée un feedback,
        on l'associe automatiquement à l'utilisateur connecté.
        """
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        filtrer les feedbacks par produit :
        /api/feedbacks/?product=ID
        """
        queryset = super().get_queryset()
        product_id = self.request.query_params.get("product")
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        # Workflow selon payment_type
        if payment.payment_type == "premium":
            seller_profile = self.request.user.seller_profile
            seller_profile.is_premium = True
            seller_profile.save()

        elif payment.payment_type == "sponsorship" and payment.product:
            payment.product.is_sponsored = True
            payment.product.save()

        elif payment.payment_type == "advertisement" and payment.product:
            # Exemple simple : créer une publicité liée
            # Advertisement.objects.create(
            #     user=self.request.user,
            #     product=payment.product,
            #     amount=payment.amount,
            #     paid_at=payment.paid_at
            # )
            pass

# class SponsoredProductViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Product.objects.filter(is_sponsored=True)
#     serializer_class = SponsoredProductsSerializer