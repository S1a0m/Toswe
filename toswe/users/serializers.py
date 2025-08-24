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



