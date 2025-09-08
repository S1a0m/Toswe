from datetime import datetime, timedelta

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

    class Meta:
        model = Product
        fields = ["id", "name", "price", "main_image", "short_description", "total_rating", "status", "is_sponsored"]

    def get_main_image(self, obj):
        main_img = obj.images.filter(is_main_image=True).first()
        if main_img:
            return ProductImageSerializer(main_img).data
        return None

    def get_total_rating(self, obj):
        stats = obj.feedback_set.aggregate(avg=Avg("rating"), count=Count("id"))
        return {
            "average": round(stats["avg"], 1) if stats["avg"] else 0,
            "count": stats["count"]
        }

    def get_short_description(self, obj):
        max_length = 80  # nombre max de caractères
        if len(obj.description) > max_length:
            return obj.description[:max_length] + "..."
        return obj.description

    def get_status(self, obj):
        """Calcule dynamiquement le statut du produit"""
        now = timezone.now()

        # 1. Promo (⚠️ à adapter selon ton modèle de promo)
        if hasattr(obj, "promotion") and obj.promotion.is_active:
            return "promo"

        # 2. Popularité (beaucoup d’ajouts au panier)
        cart_count = CartItem.objects.filter(product=obj).count()
        if cart_count >= 10:  # seuil à ajuster
            return "popular"

        # 3. Produit récent
        if obj.created_at >= now - timedelta(days=30):
            return "new"

        # 4. Par défaut, renvoyer celui en base
        return obj.status

class AdSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ad
        fields = ["id", "title", "description", "image", "is_active", "created_at", "updated_at", "product"]


class ProductDetailsSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    videos = ProductVideoSerializer(many=True, read_only=True)
    total_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "seller", "name", "price", "total_rating", "description", "images", "videos", "is_sponsored"]

    def get_total_rating(self, obj):
        stats = obj.feedback_set.aggregate(avg=Avg("rating"), count=Count("id"))
        return {
            "average": round(stats["avg"], 1) if stats["avg"] else 0,
            "count": stats["count"]
        }

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
    product = ProductCartSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product",
        write_only=True
    )

    class Meta:
        model = CartItem
        fields = ["id", "product", "product_id", "quantity"]


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
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source="product",
        write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_id", "quantity", "price"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id", "user", "phone_number", "contact_method", "address",
            "status", "created_at", "items"
        ]
        read_only_fields = ["id", "user", "status", "created_at"]

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

        from toswe.utils import generate_order_pdf
        pdf_content = generate_order_pdf(order)
        order.pdf.save(f"order_{order.id}.pdf", pdf_content)
        order.save()

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
