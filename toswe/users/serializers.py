from rest_framework.serializers import ModelSerializer, SerializerMethodField
from users.models import *

from toswe.users.models import CartItem


class UserConnexionSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['racine_id']


class ProductDetailsSerializer(ModelSerializer):
    seller = UserConnexionSerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class ProductSuggestionsSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image']


class AnnouncementsProductsSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'announcement_text']

class UserCartItemSerializer(ModelSerializer):
    class Meta:
        model = CartItem

class UserCartSerializer(ModelSerializer):
    user = UserConnexionSerializer(read_only=True)
    cart_item = UserCartItemSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'


class UserFeedbackSerializer(ModelSerializer):
    user = UserConnexionSerializer(read_only=True)
    product = ProductDetailsSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = '__all__'


class UsersProductFeedbackSerializer(ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class UserNotificationsSerializer(ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class UserOrdersSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class UserOrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class UserDeliverySerializer(ModelSerializer):
    order = UserOrderSerializer(read_only=True)

    class Meta:
        model = Delivery
        fields = '__all__'


class UserDeliveriesSerializer(ModelSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'


class UserPaymentSerializer(ModelSerializer):
    order = UserOrderSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'


class SearchProductsSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'image']


class BecomeSellerSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'is_seller', 'store_name', 'store_description']


class SellerProductsSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class SponsoredProductsSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image', 'is_sponsored']


class BecomePremiumSellerSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'is_premium', 'premium_since']


class SellerStatisticsSerializer(ModelSerializer):
    total_sales = SerializerMethodField()
    total_orders = SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'store_name', 'total_sales', 'total_orders']

    def get_total_sales(self, obj):
        return obj.orders.aggregate(total=models.Sum('total_amount'))['total'] or 0

    def get_total_orders(self, obj):
        return obj.orders.count()


