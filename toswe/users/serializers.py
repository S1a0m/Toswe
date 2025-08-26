from rest_framework import serializers
from users.models import CustomUser, Feedback, Notification, SellerProfile
from products.models import Product, Order, Delivery, Payment


class UserConnexionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'phone', 'session_mdp', 'is_authenticated', 'is_seller']

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        fields = ['id', 'shop_name', 'slogan']

class BecomeSellerSerializer(serializers.ModelSerializer):
    shop_name = serializers.CharField(required=True, max_length=100)
    logo = serializers.ImageField(required=False)
    slogan = serializers.CharField(required=False, allow_blank=True, max_length=255)
    about = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    categories = serializers.CharField(required=False)

    class Meta:
        model = SellerProfile
        fields = ["shop_name", "logo", "slogan", "about", "categories", "address"]

    def create(self, validated_data):
        user = self.context["request"].user
        # update ou create
        profile, created = SellerProfile.objects.update_or_create(
            user=user,
            defaults={
                "shop_name": validated_data["shop_name"],
                "logo": validated_data.get("logo"),
                "slogan": validated_data.get("slogan", ""),
                "about": validated_data["about"],
                "category": validated_data.get("categories"),
            }
        )
        user.is_seller = True
        user.address = validated_data["address"]
        user.save()
        return profile

class UserFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'user', 'message', 'created_at']


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



