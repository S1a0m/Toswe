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
from products.models import Product, Cart, Order, Delivery, Payment, CartItem, Ad, Promotion, OrderItem, Announcement, OfferSubscription
from users.serializers import *

from products.serializers import *

from toswe.permissions import IsUserAuthenticated

from decimal import Decimal, ROUND_DOWN

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
        return super().get_serializer_class()

    def perform_create(self, serializer):
        # serializer.create() s'occupe du seller depuis request context, donc juste save avec context injecté automatiquement
        serializer.save()

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def suggestions(self, request):
        user = request.user if request.user and request.user.is_authenticated else None
        category_id = request.query_params.get("category")

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

        products = Product.objects.filter(
            mode="published",
            is_online=True,
        )

        if category_id and str(category_id).isdigit() and int(category_id) != 0:
            products = products.filter(category__id=int(category_id))

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
                Case(When(category__in=top_categories, then=Value(5)),
                    default=Value(0), output_field=IntegerField()) +
                Case(When(id__in=sponsored_ids, then=Value(4)),
                    default=Value(0), output_field=IntegerField()) +
                Case(When(id__in=promo_ids, then=Value(3)),
                    default=Value(0), output_field=IntegerField()) +
                Case(When(id__in=popular_ids, then=Value(2)),
                    default=Value(0), output_field=IntegerField()) +
                Case(When(created_at__gte=now - timedelta(days=30), then=Value(1)),
                    default=Value(0), output_field=IntegerField())
            )
        ).order_by("-priority", "-created_at")

        # ✅ Fallback UNIQUEMENT si aucun filtre catégorie n'est actif
        # Si une catégorie est spécifiée et vide → on renvoie [] proprement
        if not products.exists() and not category_id:
            products = Product.objects.filter(
                mode="published", is_online=True
            ).order_by("-created_at")

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
        user = request.user
        try:
            product = self.get_object()
            if product.qr_code and product.seller.user == user:
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

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def scan_product(self, request):
        signed_id = request.query_params.get("signed_id")
        print("SIGNED ID:", signed_id)
        if not signed_id:
            return Response({"error": "signed_id manquant"}, status=400)
        try:
            product_id = signing.loads(signed_id)
            print("Product ID:", product_id)
            product = Product.objects.get(id=product_id)

            serializer = ProductSearchSerializer(
                product, context={"request": request}
            )
            return Response(serializer.data)
        except signing.BadSignature:
            return Response({"error": "QR code invalide"}, status=400)
        except Product.DoesNotExist:
            return Response({"error": "Produit introuvable"}, status=404)


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
        """
        Recherche textuelle avec tri optionnel.
        Query params :
        ?q=<texte>          → filtre par nom (insensible à la casse)
        ?sort=rating        → tri par note décroissante
        ?sort=price_asc     → tri par prix croissant
        ?sort=price_desc    → tri par prix décroissant
        ?sort=new           → tri par date (plus récent en premier, défaut)
        ?max_price=<int>    → filtre prix max
        ?in_stock=true      → uniquement les produits en stock
        """
        from django.db.models import Avg, Count, OuterRef, Subquery, FloatField
        from django.db.models.functions import Coalesce
    
        query     = request.query_params.get("q", "").strip()
        sort      = request.query_params.get("sort", "new")
        max_price = request.query_params.get("max_price")
        in_stock  = request.query_params.get("in_stock")
    
        if not query:
            return Response(
                {"error": "Veuillez fournir un nom de produit (paramètre ?q=)."},
                status=status.HTTP_400_BAD_REQUEST,
            )
    
        products = (
            Product.objects
            .filter(name__icontains=query, mode="published", is_online=True)
            .select_related("seller__user")
            .prefetch_related("images", "promotions", "ads")
        )
    
        # ── Filtres optionnels ────────────────────────────────────
        if max_price:
            try:
                products = products.filter(price__lte=int(max_price))
            except ValueError:
                pass
    
        if in_stock == "true":
            products = products.filter(in_stock=True)
    
        # ── Tri ───────────────────────────────────────────────────
        if sort == "rating":
            # Annotation de la note moyenne sur les feedbacks
            products = products.annotate(
                avg_rating=Coalesce(
                    Avg("feedback__rating", output_field=FloatField()),
                    0.0,
                )
            ).order_by("-avg_rating", "-created_at")
    
        elif sort == "price_asc":
            products = products.order_by("price", "-created_at")
    
        elif sort == "price_desc":
            products = products.order_by("-price", "-created_at")
    
        else:  # "new" ou défaut
            products = products.order_by("-created_at")
    
        serializer = ProductSearchSerializer(
            products, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
            
    
    @action(detail=True, methods=["delete"], url_path="delete", permission_classes=[IsAuthenticated])
    def delete_product(self, request, pk=None):
        """Suppression d’un produit par son propriétaire"""
        try:
            product = self.get_object()
            # Vérifier que l’utilisateur est bien le vendeur du produit
            if product.seller.user != request.user:
                return Response({"detail": "Vous ne pouvez supprimer que vos propres produits."}, status=403)
            product.delete()
            return Response({"detail": "Produit supprimé avec succès."}, status=204)
        except Product.DoesNotExist:
            return Response({"detail": "Produit introuvable."}, status=404)
        
 
    # ── Liste des produits du vendeur connecté ────────────────
    @action(detail=False, methods=["get"], url_path="my_products")
    def my_products(self, request):
        """
        Retourne les produits du vendeur connecté.
        Query params :
          ?mode=draft|published    → filtre par mode
          ?in_stock=false          → seulement les produits épuisés
          ?promoted=true           → seulement les produits en promotion active
        """
        user = request.user
        if not hasattr(user, "seller_profile"):
            return Response(
                {"detail": "Vous n'êtes pas un vendeur."}, status=403
            )
 
        seller = user.seller_profile
        qs = Product.objects.filter(seller=seller).prefetch_related(
            "images", "promotions"
        )
 
        # Filtres optionnels
        mode = request.query_params.get("mode")
        if mode in ("draft", "published"):
            qs = qs.filter(mode=mode)
 
        in_stock = request.query_params.get("in_stock")
        if in_stock == "false":
            qs = qs.filter(in_stock=False)
 
        promoted = request.query_params.get("promoted")
        if promoted == "true":
            qs = qs.filter(
                promotions__ended_at__gte=timezone.now()
            ).distinct()
 
        qs = qs.order_by("-created_at")
        serializer = SellerProductSerializer(
            qs, many=True, context={"request": request}
        )
        return Response(serializer.data)
 
    # ── Détail d'un produit vendeur ───────────────────────────
    @action(detail=True, methods=["get"], url_path="my_detail")
    def my_detail(self, request, pk=None):
        product = self.get_object()
        if product.seller.user != request.user:
            return Response({"detail": "Accès refusé."}, status=403)
        serializer = SellerProductSerializer(
            product, context={"request": request}
        )
        return Response(serializer.data)
 
    # ── Créer / mettre à jour un produit ─────────────────────
    # (utilise create/update natifs du ModelViewSet)
    # Override perform_create pour lier au vendeur connecté
    def perform_create(self, serializer):
        user = self.request.user
        if not hasattr(user, "seller_profile"):
            raise PermissionError("Vous n'êtes pas un vendeur.")
        serializer.save(seller=user.seller_profile)
 
    # ── Toggle publication ────────────────────────────────────
    @action(detail=True, methods=["post"], url_path="toggle_mode")
    def toggle_mode(self, request, pk=None):
        """Bascule entre draft et published."""
        product = self.get_object()
        if product.seller.user != request.user:
            return Response({"detail": "Accès refusé."}, status=403)
        product.mode = "published" if product.mode == "draft" else "draft"
        product.save()
        return Response({"mode": product.mode})
 
    # ── Toggle stock ──────────────────────────────────────────
    @action(detail=True, methods=["post"], url_path="toggle_stock")
    def toggle_stock(self, request, pk=None):
        """Marque le produit en stock ou hors stock."""
        product = self.get_object()
        if product.seller.user != request.user:
            return Response({"detail": "Accès refusé."}, status=403)
        product.in_stock = not product.in_stock
        product.save()
        return Response({"in_stock": product.in_stock})
 
    # ── Créer une promotion ───────────────────────────────────
    @action(detail=True, methods=["post"], url_path="add_promotion")
    def add_promotion(self, request, pk=None):
        """
        Body JSON :
          {
            "discount_percent": 20,       # OU
            "discount_price": 5000,
            "duration_days": 7            # optionnel, défaut 30
          }
        """
        product = self.get_object()
        if product.seller.user != request.user:
            return Response({"detail": "Accès refusé."}, status=403)
 
        # Annule les promos actives existantes
        Promotion.objects.filter(
            product=product, ended_at__gte=timezone.now()
        ).update(ended_at=timezone.now())
 
        discount_percent = request.data.get("discount_percent")
        discount_price = request.data.get("discount_price")
        duration_days = int(request.data.get("duration_days", 30))
 
        if not discount_percent and not discount_price:
            return Response(
                {"detail": "Fournir discount_percent ou discount_price."},
                status=400,
            )
 
        promo = Promotion.objects.create(
            product=product,
            discount_percent=discount_percent,
            discount_price=discount_price,
            ended_at=timezone.now() + timedelta(days=duration_days),
        )
 
        return Response(
            {
                "id": promo.id,
                "discount_percent": promo.discount_percent,
                "discount_price": str(promo.discount_price),
                "ended_at": promo.ended_at,
            },
            status=201,
        )
 
    # ── Annuler la promotion active ───────────────────────────
    @action(detail=True, methods=["delete"], url_path="cancel_promotion")
    def cancel_promotion(self, request, pk=None):
        product = self.get_object()
        if product.seller.user != request.user:
            return Response({"detail": "Accès refusé."}, status=403)
 
        count, _ = Promotion.objects.filter(
            product=product, ended_at__gte=timezone.now()
        ).delete()
 
        if count == 0:
            return Response(
                {"detail": "Aucune promotion active."}, status=404
            )
        return Response({"detail": "Promotion annulée."}, status=200)


class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all().select_related("product", "product__seller")
    serializer_class = PromotionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        product = serializer.validated_data["product"]
        days = serializer.validated_data.pop("days")
        discount_percent = serializer.validated_data["discount_percent"]

        # Vérifie que l’utilisateur connecté est bien le vendeur du produit
        if not hasattr(product, "seller") or product.seller.user != self.request.user:
            raise serializers.ValidationError(
                "Vous ne pouvez créer une promotion que pour vos propres produits."
            )

        # Calcul du prix remisé
        discount_price = product.price * (100 - discount_percent) / 100

        # Calcul de la date de fin
        ended_at = now() + timedelta(days=days)

        serializer.save(
            discount_price=discount_price,
            ended_at=ended_at
        )


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
        queryset = self.get_queryset().filter(ad_type="generic", ended_at__gte=now())
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
            ad_type='generic',
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
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()  # ça crée l'order peu importe

        if not request.user.is_authenticated:
            # 🔹 Retourne juste un message, sans les détails de l'order
            return Response(
                {"message": "Commande enregistrée. Connectez-vous pour voir vos commandes."},
                status=status.HTTP_200_OK
            )

        # 🔹 Sinon (authentifié) → comportement normal
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
        elif hasattr(user, "seller_profile"):
            # cas vendeur
            seller_profile = user.seller_profile
            if not instance.items.filter(product__seller=seller_profile).exists():
                return Response({"detail": "Vous n’avez pas accès à cette commande."}, status=403)
        else:
            return Response({"detail": "Vous n’avez pas accès à cette commande."}, status=403)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    

    @action(detail=True, methods=["get"])
    def for_seller(self, request, pk=None):
        """
        Détail d'une commande mais limité aux produits du vendeur connecté.
        """
        user = request.user
        if not hasattr(user, "seller_profile"):
            return Response({"detail": "Accès réservé aux vendeurs."}, status=403)

        order = get_object_or_404(Order, pk=pk)

        # Vérifier que la commande contient bien au moins un produit de ce vendeur
        if not order.items.filter(product__seller=user.seller_profile).exists():
            return Response(
                {"detail": "Aucun produit de cette commande ne vous appartient."},
                status=403
            )

        serializer = OrderForSellerSerializer(order, context={"request": request})
        return Response(serializer.data)


    @action(detail=False, methods=["get"])
    def as_seller(self, request):
        """
        Liste toutes les commandes contenant au moins un produit du vendeur connecté.
        """
        user = request.user
        if not user.is_authenticated or not hasattr(user, "seller_profile"):
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

    @action(detail=False, methods=["get"])
    def my_balance(self, request):
        """
        Solde disponible du vendeur connecté.
        Commission calculée selon l'offre active :
          Pro    → 2%
          Boost  → 5%
          Basic  → 10% (même taux que sans offre)
          Aucune → 10%
        Seuls les OrderItem livrés et non encore payés sont inclus.
        """
        user = request.user
 
        if not hasattr(user, "seller_profile"):
            return Response({"detail": "Pas vendeur"}, status=403)
 
        seller = user.seller_profile
 
        # ── Taux de commission réel depuis l'offre active ──────
        commission_rate = Decimal("0.10")   # défaut : 10%
 
        active_sub = (
            OfferSubscription.objects
            .filter(
                seller=seller,
                status="active",
                expires_at__gt=timezone.now(),
            )
            .select_related("offer")
            .first()
        )
 
        if active_sub:
            commission_rate = (
                active_sub.offer.commission_percent / Decimal("100")
            )
 
        # ── Calcul du solde ────────────────────────────────────
        items = OrderItem.objects.filter(
            product__seller=seller,
            order__status="delivered",
            seller_paid=False,
        )
 
        total_sales          = Decimal("0")
        total_commission     = Decimal("0")
        total_seller_revenue = Decimal("0")
 
        for item in items:
            price    = item.price
            quantity = item.quantity
 
            commission_per_unit = (price * commission_rate).quantize(
                Decimal("1"), rounding=ROUND_DOWN
            )
            seller_net_per_unit = price - commission_per_unit
 
            total_sales          += price * quantity
            total_commission     += commission_per_unit * quantity
            total_seller_revenue += seller_net_per_unit * quantity
 
        return Response({
            "total_sales":       int(total_sales),
            "commission":        int(total_commission),
            "available_balance": int(total_seller_revenue),
            # Infos affichées dans le dashboard vendeur Flutter
            "commission_rate":   f"{int(commission_rate * 100)}%",
            "offer_name":        active_sub.offer.name if active_sub else None,
            "offer_expires_at":  active_sub.expires_at if active_sub else None,
        })
 
    @action(detail=False, methods=["post"])
    def mark_seller_paid(self, request):
        """
        Marque tous les OrderItem livrés du vendeur comme payés.
        À appeler après validation d'un retrait par l'admin.
        """
        seller = request.user.seller_profile
 
        items = OrderItem.objects.filter(
            product__seller=seller,
            order__status="delivered",
            seller_paid=False,
        )
 
        count = items.count()
        items.update(
            seller_paid=True,
            seller_paid_at=timezone.now(),
        )
 
        return Response({
            "detail": f"{count} item(s) marqué(s) comme payés.",
        })
 
    
    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        """
        Permet à l’acheteur d’annuler sa commande.
        """
        order = get_object_or_404(Order, pk=pk)

        # Vérifier que l’utilisateur est bien l’acheteur
        if order.user != request.user:
            return Response(
                {"detail": "Vous ne pouvez pas annuler cette commande."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Vérifier que la commande n’est pas déjà expédiée ou annulée
        if order.status in ["shipped", "canceled"]:
            return Response(
                {"detail": f"Impossible d’annuler une commande déjà {order.status}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Annuler
        order.status = "cancelled"
        order.save()
        Notification.objects.create(
            user=request.user,
            title="Commande",
            message=f"Vous venez d'annuler la commande #{order.id}."
        )
        

        return Response(
            {"detail": "Commande annulée avec succès."},
            status=status.HTTP_200_OK
        )


class SellerOfferViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/seller-offers/          → liste des offres actives
    GET /api/seller-offers/{id}/     → détail d'une offre
    POST /api/seller-offers/subscribe/  → souscrire à une offre
    GET  /api/seller-offers/my_subscription/ → abonnement courant du vendeur
    """
    queryset = SellerOffer.objects.filter(is_active=True).order_by("price")
    serializer_class = SellerOfferSerializer
    permission_classes = [AllowAny]
 
    # ── Souscrire à une offre ─────────────────────────────────
    @action(
        detail=False, methods=["post"],
        permission_classes=[IsAuthenticated],
        url_path="subscribe",
    )
    def subscribe(self, request):
        serializer = SubscribeOfferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
 
        user = request.user
        seller = getattr(user, "seller_profile", None)
        if not seller:
            return Response(
                {"detail": "Vous n'êtes pas un vendeur."},
                status=status.HTTP_403_FORBIDDEN,
            )
 
        # Récupère l'offre
        try:
            offer = SellerOffer.objects.get(
                id=data["offer_id"], is_active=True
            )
        except SellerOffer.DoesNotExist:
            return Response(
                {"detail": "Offre introuvable ou inactive."},
                status=status.HTTP_404_NOT_FOUND,
            )
 
        # ── Paiement ────────────────────────────────────────
        payment_method = data["payment_method"]
        phone = data["phone_number"]
 
        if payment_method == "moov_money":
            success = PaymentGateway.pay_with_moov(phone, offer.price)
        else:
            success = PaymentGateway.pay_with_mtn(phone, offer.price)
 
        if not success:
            return Response(
                {"detail": "Échec du paiement. Vérifie ton solde et réessaie."},
                status=status.HTTP_402_PAYMENT_REQUIRED,
            )
 
        # ── Désactive l'abonnement actif précédent ───────────
        OfferSubscription.objects.filter(
            seller=seller, status="active"
        ).update(status="cancelled")
 
        # ── Crée le nouvel abonnement ────────────────────────
        now = timezone.now()
        sub = OfferSubscription.objects.create(
            seller=seller,
            offer=offer,
            status="active",
            payment_method=payment_method,
            phone_number=phone,
            amount_paid=offer.price,
            starts_at=now,
            expires_at=now + timedelta(days=offer.duration_days),
        )
 
        # ── Notification in-app ──────────────────────────────
        Notification.objects.create(
            user=user,
            title=f"Offre {offer.name} activée 🎉",
            message=(
                f"Votre offre {offer.name} est maintenant active jusqu'au "
                f"{sub.expires_at.strftime('%d/%m/%Y')}. "
                f"Profitez de {offer.commission_percent}% de commission seulement !"
            ),
        )
 
        # ── Email de confirmation ────────────────────────────
        _send_offer_confirmation_email(user, offer, sub)
 
        return Response(
            OfferSubscriptionSerializer(sub).data,
            status=status.HTTP_201_CREATED,
        )
 
    # ── Abonnement courant du vendeur ─────────────────────────
    @action(
        detail=False, methods=["get"],
        permission_classes=[IsAuthenticated],
        url_path="my_subscription",
    )
    def my_subscription(self, request):
        seller = getattr(request.user, "seller_profile", None)
        if not seller:
            return Response({"detail": "Pas vendeur."}, status=403)
 
        sub = (
            OfferSubscription.objects
            .filter(seller=seller, status="active",
                    expires_at__gt=timezone.now())
            .select_related("offer")
            .first()
        )
        if not sub:
            return Response({"subscription": None})
 
        return Response({"subscription": OfferSubscriptionSerializer(sub).data})
 
 
    # ── Helper email ──────────────────────────────────────────────
    
def _send_offer_confirmation_email(user, offer, sub):
        """Envoie un email HTML de confirmation de souscription."""
        send_email(
            f"Offre {offer.name} activée sur Tôswè Africa 🎉",
            f"""
            <html>
            <head>
            <style>
                body {{ font-family: 'Helvetica Neue', sans-serif;
                    background:#fdf8f5; margin:0; padding:0; }}
                .wrap {{ max-width:600px; margin:24px auto; background:#fff;
                        border-radius:16px; overflow:hidden;
                        box-shadow:0 4px 16px rgba(0,0,0,.08); }}
                .header {{ background:linear-gradient(135deg,#7D260F,#C65A2E);
                        padding:28px; text-align:center; color:#fff; }}
                .header h1 {{ margin:0; font-size:22px; letter-spacing:.5px; }}
                .body {{ padding:32px; color:#333; line-height:1.7; font-size:15px; }}
                .card {{ background:#fdf8f5; border-radius:12px; padding:20px;
                        margin:24px 0; border:1px solid #f0e8e0; }}
                .card h2 {{ margin:0 0 8px; color:#C65A2E; font-size:20px; }}
                .tag {{ display:inline-block; background:#C65A2E; color:#fff;
                        padding:4px 12px; border-radius:20px; font-size:13px;
                        font-weight:700; margin-bottom:12px; }}
                .feature {{ display:flex; align-items:center; gap:10px;
                            padding:6px 0; color:#3E2C23; font-size:14px; }}
                .check {{ color:#C65A2E; font-size:16px; }}
                .footer {{ text-align:center; font-size:11px; color:#999;
                        padding:20px; }}
            </style>
            </head>
            <body>
            <div class="wrap">
                <div class="header">
                <h1>Tôswè Africa</h1>
                </div>
                <div class="body">
                <p>Bonjour <strong>{user.username}</strong> 👋🏽,</p>
                <p>Votre offre <strong>{offer.name}</strong> a été activée avec succès !</p>
    
                <div class="card">
                    <div class="tag">{offer.name}</div>
                    <h2>{offer.price} CFA</h2>
                    <p style="color:#7A7570;margin:0 0 12px;">
                    Valable jusqu'au <strong>{sub.expires_at.strftime("%d/%m/%Y")}</strong>
                    &nbsp;·&nbsp; Commission : <strong>{offer.commission_percent}%</strong>
                    </p>
                    {''.join(f'<div class="feature"><span class="check">✓</span>{f}</div>'
                            for f in offer.features)}
                </div>
    
                <p>Nehanda va maintenant booster votre boutique.
                    Bonne vente ! 🚀</p>
                </div>
                <div class="footer">
                © 2025 Tôswè Africa — Tous droits réservés.
                </div>
            </div>
            </body>
            </html>
            """,
            user.email,
        )


class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset           = Announcement.objects.filter(active=True)
    serializer_class   = AnnouncementSerializer
    permission_classes = [AllowAny]


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