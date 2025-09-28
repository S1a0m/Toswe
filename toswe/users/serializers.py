from django.db.models import Avg, Count
from rest_framework import serializers
from users.models import CustomUser, Notification, SellerProfile, SellerStatistics
from products.models import Product, Order, Delivery, Payment, Feedback
from toswe.utils import send_email


class UserConnexionSerializer(serializers.ModelSerializer):
    is_seller = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['id', 'phone', 'session_mdp', 'is_authenticated', 'is_seller']

    def get_is_gamer(self, obj):
        return hasattr(obj, 'seller_profile')

class BrandSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    seller_id = serializers.SerializerMethodField()
    class Meta:
        model = SellerProfile
        fields = ['id', 'shop_name', 'logo', 'slogan', 'rating', 'seller_id']

    def get_rating(self, obj):
        # Récupérer tous les produits du vendeur
        products = obj.product_set.all()

        # Agréger la moyenne et le nombre d'avis
        stats = Feedback.objects.filter(product__in=products).aggregate(
            avg=Avg("rating"), count=Count("id")
        )

        return round(stats["avg"], 1) if stats["avg"] else 0

    def get_seller_id(self, obj):
        return obj.user.id


class SellerListSerializer(serializers.ModelSerializer):
    total_subscribers = serializers.SerializerMethodField()
    seller_user_id = serializers.SerializerMethodField()

    class Meta:
        model = SellerProfile
        fields = ['id', 'seller_user_id', 'shop_name', 'logo', 'total_subscribers', 'is_verified', 'is_brand']

    def get_seller_user_id(self, obj):
        return obj.user.id

    def get_total_subscribers(self, obj):
        return obj.subscribers.count()


class ShopHeaderSerializer(serializers.ModelSerializer):
    seller_essential = SellerListSerializer(source='*', read_only=True)
    total_rating = serializers.SerializerMethodField()

    class Meta:
        model = SellerProfile
        fields = ['seller_essential', 'slogan', 'about', 'total_rating', 'is_verified']

    def get_total_rating(self, obj):
        # Récupérer tous les produits du vendeur
        products = obj.product_set.all()

        # Agréger la moyenne et le nombre d'avis
        stats = Feedback.objects.filter(product__in=products).aggregate(
            avg=Avg("rating"), count=Count("id")
        )

        return {
            "average": round(stats["avg"], 1) if stats["avg"] else 0,
            "count": stats["count"] or 0
        }



class BecomeSellerSerializer(serializers.ModelSerializer):
    shop_name = serializers.CharField(required=True, max_length=100)
    logo = serializers.ImageField(required=False)
    slogan = serializers.CharField(required=False, allow_blank=True, max_length=255)
    about = serializers.CharField(required=True)
    #address = serializers.CharField(required=True)

    class Meta:
        model = SellerProfile
        fields = ["shop_name", "logo", "slogan", "about"]#, "address"]

    def create(self, validated_data):
        user = self.context["request"].user

        # update_or_create 
        profile, created = SellerProfile.objects.update_or_create(
            user=user,
            defaults={
                "shop_name": validated_data["shop_name"],
                "logo": validated_data.get("logo"),
                "slogan": validated_data.get("slogan", ""),
                "about": validated_data["about"],
            }
        )

        message = f"L'utilisateur {user.username} demande à devenir vendeur."

        # Marquer l’utilisateur comme vendeur
        # user.is_seller = True
        # user.address = validated_data["address"]
        send_email("Demande", message, "remveille@gmail.com")
        user.save()

        return profile



class UserNotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'is_read', 'created_at', 'detail_link']


class UserLiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "phone")


class SellerStatisticsSerializer(serializers.ModelSerializer):
    # champs calculés/agrégés
    total_products = serializers.SerializerMethodField()
    total_orders = serializers.SerializerMethodField()

    class Meta:
        model = SellerStatistics
        fields = [
            "id",
            "total_products",
            "total_orders",
            "total_subscribers",
            "total_income",
            "average_order_value",
            "last_sale_date",
            "best_selling_product_name",
            "best_selling_product_id",
        ]
        read_only_fields = fields

    def get_total_products(self, obj):
        # obj.seller est un SellerProfile
        return Product.objects.filter(seller=obj.seller).count()

    def get_total_orders(self, obj):
        # suppose que Order a un FK vers Product: Order.product
        return Order.objects.filter(product__seller=obj.seller).count()


class SellerProfileSerializer(serializers.ModelSerializer):
    user = UserLiteSerializer(read_only=True)
    logo = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    subscribers_count = serializers.SerializerMethodField()
    products_count = serializers.SerializerMethodField()
    stats = serializers.SerializerMethodField()

    class Meta:
        model = SellerProfile
        fields = [
            "id",
            "user",
            "shop_name",
            "slogan",
            "about",
            "logo",
            "is_brand",
            "is_verified",
            "is_premium",
            "show_on_market",
            "rating",
            "categories",
            "subscribers_count",
            "products_count",
            "stats",
        ]
        read_only_fields = [
            "id",
            "user",
            "logo",
            "subscribers_count",
            "products_count",
            "stats",
        ]

    def get_logo(self, obj):
        """
        Retourne une URL absolue si possible (préserve la compatibilité avec le front).
        Evite d'exposer le FileField brut qui pourrait causer le UnicodeDecodeError.
        """
        if not obj.logo:
            return None
        request = self.context.get("request")
        try:
            url = obj.logo.url # request.build_absolute_uri(obj.logo.url)
        except Exception:
            return None
        if request:
            return request.build_absolute_uri(url)
        # fallback: renvoyer l'url relative
        return url

    def get_categories(self, obj):
        # renvoie liste de noms (ou tuples id/name si tu préfères)
        return [c.name for c in obj.categories.all()]

    def get_subscribers_count(self, obj):
        return obj.subscribers.count()

    def get_products_count(self, obj):
        return Product.objects.filter(seller=obj).count()

    def get_stats(self, obj):
        # si un SellerStatistics est lié, sérialise-le, sinon None
        stats = getattr(obj, "stats", None)
        if stats:
            return SellerStatisticsSerializer(stats, context=self.context).data
        return None




