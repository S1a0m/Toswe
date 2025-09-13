from django.db.models import Avg, Count
from rest_framework import serializers
from users.models import CustomUser, Notification, SellerProfile
from products.models import Product, Order, Delivery, Payment, Feedback


class UserConnexionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'phone', 'session_mdp', 'is_authenticated', 'is_seller']

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
        fields = ['id', 'seller_user_id', 'shop_name', 'logo', 'total_subscribers']

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
    categories = serializers.CharField(required=False)  # tu reçois un CSV

    class Meta:
        model = SellerProfile
        fields = ["shop_name", "logo", "slogan", "about", "categories"]#, "address"]

    def create(self, validated_data):
        user = self.context["request"].user

        # Récupérer les catégories avant
        categories_csv = validated_data.pop("categories", "")
        categories_list = []
        if categories_csv:
            category_names = [c.strip() for c in categories_csv.split(",") if c.strip()]
            from products.models import Category
            categories_list = Category.objects.filter(name__in=category_names)

        # update_or_create SANS categories
        profile, created = SellerProfile.objects.update_or_create(
            user=user,
            defaults={
                "shop_name": validated_data["shop_name"],
                "logo": validated_data.get("logo"),
                "slogan": validated_data.get("slogan", ""),
                "about": validated_data["about"],
            }
        )

        # Affecter les catégories correctement
        if categories_list:
            profile.categories.set(categories_list)

        # Marquer l’utilisateur comme vendeur
        # user.is_seller = True
        # user.address = validated_data["address"]
        user.save()

        return profile



class UserNotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'is_read', 'sent_date']


class SellerStatisticsSerializer(serializers.ModelSerializer):
    total_products = serializers.SerializerMethodField()
    total_orders = serializers.SerializerMethodField()
    total_feedbacks = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'racine_id', 'is_seller', 'is_premium',
                  'total_products', 'total_orders', 'total_feedbacks']

    def get_total_products(self, obj):
        return Product.objects.filter(seller=obj).count()

    def get_total_orders(self, obj):
        return Order.objects.filter(product__seller=obj).count()

    def get_total_feedbacks(self, obj):
        return Feedback.objects.filter(user=obj).count()



