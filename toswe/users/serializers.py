from rest_framework import serializers
from users.models import User, Feedback, Notification
from products.models import Product, Order, Delivery, Payment


class UserConnexionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'racine_id', 'is_authenticated', 'is_seller', 'is_premium']


class UserFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'user', 'message', 'created_at']


class UserNotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'title', 'message', 'is_read', 'created_at']


class SellerStatisticsSerializer(serializers.ModelSerializer):
    total_products = serializers.SerializerMethodField()
    total_orders = serializers.SerializerMethodField()
    total_feedbacks = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'racine_id', 'is_seller', 'is_premium',
                  'total_products', 'total_orders', 'total_feedbacks']

    def get_total_products(self, obj):
        return Product.objects.filter(seller=obj).count()

    def get_total_orders(self, obj):
        return Order.objects.filter(product__seller=obj).count()

    def get_total_feedbacks(self, obj):
        return Feedback.objects.filter(user=obj).count()



