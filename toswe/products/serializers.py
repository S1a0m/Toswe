from rest_framework import serializers
from products.models import Product, Cart, Order, OrderItem, Delivery, Payment, ProductImage, CartItem


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image", "is_main_image"]

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

    class Meta:
        model = Product
        fields = ["id", "name", "price", "main_image"]

    def get_main_image(self, obj):
        main_img = obj.images.filter(is_main_image=True).first()
        if main_img:
            return ProductImageSerializer(main_img).data
        return None


class ProductDetailsSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "price", "description", "images"]


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
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
