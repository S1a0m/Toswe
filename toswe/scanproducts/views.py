from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from products.models import Product
from products.serializers import ProductsSerializer
from .utils import find_similar_products
from ..products.models import Order


class ProductSearchByImageViewSet(viewsets.ViewSet):
    parser_classes = [MultiPartParser]

    @action(detail=False, methods=['post'], url_path='search-by-image')
    def search_by_image(self, request):
        image_file = request.FILES.get('image')
        if not image_file:
            return Response({'error': 'Aucune image fournie.'}, status=400)

        # Convertir en image PIL si nécessaire
        from PIL import Image
        image = Image.open(image_file).convert("RGB")

        # Appel à ton modèle ML
        similar_products = find_similar_products(image)

        # Sérialiser les résultats
        serializer = ProductsSerializer(similar_products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def quick_order(self, request):
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Produit introuvable"}, status=404)

        order = Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            total_price=product.price * int(quantity)
        )
        return Response({"message": "Commande passée", "order_id": order.id})
