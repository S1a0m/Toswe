from rest_framework import serializers
from products.models import Product, Cart, Order, OrderItem, Delivery, Payment


# === PRODUITS ===

class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductSuggestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'thumbnail', 'is_sponsored']


class AnnouncementsProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'announcement_text', 'price']


# === PANIER ===

class UserCartSerializer(serializers.ModelSerializer):
    product = ProductDetailsSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )

    class Meta:
        model = Cart
        fields = ['id', 'product', 'product_id', 'quantity', 'added_at']


# === COMMANDE ===

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductDetailsSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']


class UserOrdersSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'payment_method', 'created_at', 'items']
        read_only_fields = ['user', 'created_at']


# === LIVRAISON ===

class UserDeliveriesSerializer(serializers.ModelSerializer):
    order = UserOrdersSerializer(read_only=True)
    order_id = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(), source='order', write_only=True
    )

    class Meta:
        model = Delivery
        fields = ['id', 'order', 'order_id', 'delivery_status', 'delivered_at', 'location']


# === PAIEMENT ===

class UserPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'amount', 'payment_method', 'status', 'created_at']
