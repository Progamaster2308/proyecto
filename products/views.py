from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from .services import PricingService, ElectronicDiscountStrategy, NoDiscountStrategy

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Patrón Structural: Facade (Fachada) para simplificar la lógica de precios y descuentos
class FinalPriceFacadeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"error": "Producto no encontrado"}, status=404)

        # Selección dinámica de estrategia según la categoría (Strategy Pattern)
        if product.category.name.lower() == 'electronica':
            strategy = ElectronicDiscountStrategy()
        else:
            strategy = NoDiscountStrategy()

        # Uso de la capa de servicios a través de la Fachada
        pricing_service = PricingService(strategy)
        final_price = pricing_service.get_final_price(float(product.price))

        return Response({
            "product": product.name,
            "category": product.category.name,
            "original_price": str(product.price),
            "final_price_with_discount": round(final_price, 2)
        })    