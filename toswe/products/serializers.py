from datetime import datetime, timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from django.db.models import Avg, Count
from products.models import Product, Cart, Order, OrderItem, Delivery, Payment, ProductImage, CartItem, Feedback, ProductVideo, Category, Ad


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "is_main_image"]

class ProductVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVideo
        fields = ["id", "video"]

class ProductSearchSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()
    shop_name = serializers.CharField(source="seller.shop_name")

    class Meta:
        model = Product
        fields = ["id", "name", "price", "main_image", "shop_name"]

    def get_main_image(self, obj):
        main_img = obj.images.filter(is_main_image=True).first()
        if main_img:
            return main_img.image.url
        return None


class ProductSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()
    total_rating = serializers.SerializerMethodField()
    short_description = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    seller_id = serializers.SerializerMethodField()
    is_sponsored = serializers.SerializerMethodField()  # 🔹 calculé dynamiquement

    class Meta:
        model = Product
        fields = [
            "id",
            "seller_id",
            "name",
            "price",
            "main_image",
            "short_description",
            "total_rating",
            "status",
            "is_sponsored",
        ]

    def get_main_image(self, obj):
        main_img = obj.images.filter(is_main_image=True).first()
        if main_img:
            return ProductImageSerializer(main_img).data
        return None

    def get_seller_id(self, obj):
        return obj.seller.user.id

    def get_total_rating(self, obj):
        stats = obj.feedback_set.aggregate(avg=Avg("rating"), count=Count("id"))
        return {
            "average": round(stats["avg"], 1) if stats["avg"] else 0,
            "count": stats["count"],
        }

    def get_short_description(self, obj):
        max_length = 80
        return obj.description[:max_length] + "..." if len(obj.description) > max_length else obj.description

    def get_status(self, obj):
        now = timezone.now()

        # 1. Vérifier s’il a une promo active
        promo = obj.promotions.filter(ended_at__gte=now).first()
        if promo:
            return "promo"

        # 2. Vérifier popularité (ex: nb d’items au panier)
        cart_count = CartItem.objects.filter(product=obj).count()
        if cart_count >= 10:  # seuil ajustable
            return "popular"

        # 3. Produit récent
        if obj.created_at >= now - timedelta(days=30):
            return "new"

        return obj.status

    def get_is_sponsored(self, obj):
        """Un produit est sponsorisé si une pub active existe"""
        now = timezone.now()
        return obj.ads.filter(ad_type="sponsored", is_active=True, ended_at__gte=now).exists()

# serializers.py
from rest_framework import serializers
from .models import Promotion

class PromotionSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    seller_name = serializers.CharField(source="product.seller.shop_name", read_only=True)

    class Meta:
        model = Promotion
        fields = [
            "id",
            "product",
            "product_name",
            "seller_name",
            "discount_percent",
            "discount_price",
            "created_at",
            "ended_at",
        ]



class AdSerializer(serializers.ModelSerializer):
    seller_id = serializers.SerializerMethodField()
    class Meta:
        model = Ad
        fields = [
            "id",
            "seller_id",
            "title",
            "description",
            "image",
            "ad_type",
            "is_active",
            "created_at",
            "updated_at",
            "ended_at",
            "product",
            "amount",
        ]

    def validate(self, data):
        user = self.context["request"].user
        # seller = getattr(user, "seller_profile", None)
        seller = user.seller_profile
        print("Vendeur:?", user)
        print("Seller:?", user.seller_profile, seller)

        if not seller:
            raise serializers.ValidationError("Seuls les vendeurs peuvent créer une publicité.")

        ad_type = data.get("ad_type")

        # Règle 1 : annonces génériques → seulement premium
        if ad_type == "generic":
            if not seller.is_premium:
                raise serializers.ValidationError(
                    "Seuls les vendeurs premium peuvent créer une annonce générale."
                )
            if not data.get("title") or not data.get("description"):
                raise serializers.ValidationError(
                    "Titre et description sont obligatoires pour une annonce générale."
                )

        # Règle 2 : sponsorisation produit → max 2 / mois pour non-premium
        elif ad_type == "sponsored":
            if not data.get("product"):
                raise serializers.ValidationError("Un produit doit être lié à la sponsorisation.")

            if not seller.is_premium:
                from django.utils.timezone import now
                month_start = now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                count_ads = Ad.objects.filter(
                    ad_type="sponsored",
                    product__seller=seller,
                    created_at__gte=month_start,
                ).count()
                if count_ads >= 2:
                    raise serializers.ValidationError(
                        "Vous avez atteint la limite de 2 sponsorisations pour ce mois."
                    )

            # Supprimer champs inutiles (pas de title, image, description pour sponsorisation)
            data["title"] = None
            data["description"] = None
            data["image"] = None

        return data

    def get_seller_id(self, obj):
        return obj.seller.user.id




class ProductDetailsSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    videos = ProductVideoSerializer(many=True, read_only=True)
    total_rating = serializers.SerializerMethodField()
    seller_id = serializers.SerializerMethodField()
    is_sponsored = serializers.SerializerMethodField()
    promotion = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "seller_id",
            "seller",
            "name",
            "price",
            "total_rating",
            "description",
            "images",
            "videos",
            "is_online",
            "is_sponsored",
            "promotion",
        ]

    def get_total_rating(self, obj):
        stats = obj.feedback_set.aggregate(avg=Avg("rating"), count=Count("id"))
        return {
            "average": round(stats["avg"], 1) if stats["avg"] else 0,
            "count": stats["count"],
        }

    def get_seller_id(self, obj):
        return obj.seller.user.id

    def get_is_sponsored(self, obj):
        now = timezone.now()
        return obj.ads.filter(ad_type="sponsored", is_active=True, ended_at__gte=now).exists()

    def get_promotion(self, obj):
        """
        Retourne la promo active du produit (s’il y en a une).
        """
        now = timezone.now()
        promo = obj.promotions.filter(ended_at__gte=now).first()
        if promo:
            return {
                "id": promo.id,
                "discount_percent": promo.discount_percent,
                "discount_price": promo.discount_price,
                "ended_at": promo.ended_at,
            }
        return None


class ProductCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    videos = serializers.ListField(
        child=serializers.FileField(), write_only=True, required=False
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "category",
            "images",
            "is_online",
            "videos",
            "status",
        ]
        read_only_fields = ["id"]

    def validate_price(self, value):
        if value is None or value < 0:
            raise serializers.ValidationError("Le prix doit être un entier positif.")
        return value

    def validate(self, attrs):
        request = self.context.get("request")
        user = getattr(request, "user", None)

        if not user or not user.is_authenticated:
            raise serializers.ValidationError("Utilisateur non authentifié.")

        seller_profile = getattr(user, "seller_profile", None)
        if not seller_profile:
            raise serializers.ValidationError("Impossible : utilisateur non vendeur.")

        # Vérification du quota de produits
        current_count = seller_profile.product_set.count()
        if seller_profile.is_premium:
            if current_count >= 500:
                raise serializers.ValidationError("Limite de 500 produits atteinte pour les vendeurs premium.")
        else:
            if current_count >= 20:
                raise serializers.ValidationError("Limite de 20 produits atteinte pour les vendeurs non premium.")

            # Vérification restriction vidéos
            if "videos" in attrs and attrs["videos"]:
                raise serializers.ValidationError("Les vendeurs non premium ne peuvent pas ajouter de vidéos.")

        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        images = validated_data.pop("images", [])
        videos = validated_data.pop("videos", [])

        seller_profile = getattr(request.user, "seller_profile", None)
        if not seller_profile:
            raise serializers.ValidationError("Impossible : utilisateur non vendeur.")

        with transaction.atomic():
            product = Product.objects.create(seller=seller_profile, **validated_data)

            # Images
            for idx, f in enumerate(images):
                ProductImage.objects.create(
                    product=product,
                    image=f,
                    is_main_image=(idx == 0)
                )

            # Vidéos (si premium uniquement → déjà validé dans `validate`)
            for f in videos:
                ProductVideo.objects.create(product=product, video=f)

        return product




class AdDetailsSerializer(serializers.ModelSerializer):
    product = ProductDetailsSerializer(read_only=True)  # ⚡ on sérialise le produit lié

    class Meta:
        model = Ad
        fields = [
            "id",
            "title",
            "description",
            "image",
            "is_active",
            "created_at",
            "updated_at",
            "product",
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]

class FeedbackSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    class Meta:
        model = Feedback
        fields = ["id", "product", "user_name", "rating", "comment", "created_at"]

    def get_user_name(self, obj):
        return obj.user.username

class ProductCartSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ["id", "name", "price", "main_image"]

    def get_main_image(self, obj):
        main_img = obj.images.filter(is_main_image=True).first()
        if main_img:
            return ProductImageSerializer(main_img).data
        return None


class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product",
        # write_only=True
    )

    # champs calculés à plat
    name = serializers.CharField(source="product.name", read_only=True)
    price = serializers.DecimalField(source="product.price", max_digits=10, decimal_places=2, read_only=True)
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "product_id", "name", "price", "main_image", "quantity"]

    def get_main_image(self, obj):
        main_img = obj.product.images.filter(is_main_image=True).first()
        return main_img.image.url if main_img else None



class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "items", "created_at"]
        read_only_fields = ["id", "user", "created_at"]

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        cart = Cart.objects.create(**validated_data)
        for item in items_data:
            CartItem.objects.create(cart=cart, **item)
        return cart

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", [])
        instance.save()

        # ⚡ simplification : on vide puis on recrée les items
        instance.items.all().delete()
        for item in items_data:
            CartItem.objects.create(cart=instance, **item)

        return instance




# === COMMANDE ===

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    main_image = serializers.SerializerMethodField()
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product",
        write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_id", "quantity", "price", "main_image"]

    def get_main_image(self, obj):
        main_img = obj.product.images.filter(is_main_image=True).first()
        return main_img.image.url if main_img else None

class OrderListSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ["id", "user", "status", "created_at", "total"]

    def get_total(self, obj):
        return sum(item.price * item.quantity for item in obj.items.all())


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id", "user", "phone_number", "contact_method", "address",
            "status", "created_at", "total", "items", "pdf"
        ]
        read_only_fields = ["id", "user", "status", "created_at"]

    def get_total(self, obj):
        return sum(item.price * item.quantity for item in obj.items.all())

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        user = self.context["request"].user if self.context["request"].user.is_authenticated else None

        order = Order.objects.create(user=user, **validated_data)

        for item in items_data:
            product = item["product"]
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item["quantity"],
                price=product.price
            )

        # Génération du PDF
        from toswe.utils import generate_order_pdf
        pdf_content = generate_order_pdf(order)
        order.pdf.save(f"order_{order.id}.pdf", pdf_content)
        order.save()

        # 🔔 Envoi des notifications ICI (après ajout des items)
        from users.models import Notification, SellerProfile
        seller_ids = list(order.items.values_list("product__seller_id", flat=True).distinct())
        sellers = SellerProfile.objects.filter(id__in=seller_ids)

        for seller in sellers:
            notif = Notification.objects.create(
                user=seller.user,
                message=f"Nouvelle commande contenant vos produits (commande #{order.id})."
            )
            from asgiref.sync import async_to_sync
            from channels.layers import get_channel_layer
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"user_{seller.user.id}",
                {
                    "type": "send_notification",
                    "message": notif.message,
                    "timestamp": str(notif.created_at),
                }
            )

        return order


# === LIVRAISON ===

class DeliveriesSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    order_id = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(), source='order', write_only=True
    )

    class Meta:
        model = Delivery
        fields = ['id', 'order', 'order_id', 'delivery_status', 'delivered_at', 'location']


# === PAIEMENT ===

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "user", "payment_type", "method", "amount",
                  "order", "product", "advertisement",
                  "is_successful", "paid_at"]
        read_only_fields = ["id", "paid_at", "is_successful"]

    def validate(self, data):
        p_type = data.get("payment_type")

        if p_type == "order" and not data.get("order"):
            raise serializers.ValidationError("Une commande est requise pour un paiement de type 'order'.")
        if p_type == "sponsorship" and not data.get("product"):
            raise serializers.ValidationError("Un produit est requis pour une sponsorisation.")
        if p_type == "advertisement" and not data.get("advertisement"):
            raise serializers.ValidationError("Une publicité est requise pour ce paiement.")

        return data

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)
