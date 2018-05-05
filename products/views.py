from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer


"""
Viweset de Productos (CRUD)
"""

class ProductViewSet(viewsets.ModelViewSet):
	queryset = Product.objects.all().filter(in_stock=True)
	serializer_class = ProductSerializer

	#buscador y filtros
