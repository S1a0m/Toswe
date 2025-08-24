from rest_framework import serializers
from products.models import Product, Cart, Order, OrderItem, Delivery, Payment, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = ['id', 'image_url']

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None

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

# === PRODUITS ===

class ProductDetailsSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    qr_code_url = serializers.SerializerMethodField()

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
