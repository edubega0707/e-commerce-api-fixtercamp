from rest_framework import viewsets
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .pagination import ProductPagination
from django.db.models import Q


class CategoryViewSet(viewsets.ModelViewSet):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer

"""
Viweset de Productos (CRUD)
"""

class ProductViewSet(viewsets.ModelViewSet):
	queryset = Product.objects.all().filter(in_stock=True)
	serializer_class = ProductSerializer
	#pagination_class = ProductPagination
	#buscador y filtros

	def get_queryset(self, *args, **kwargs):
		category = self.request.GET.get('cat')
		search = self.request.GET.get('s')
		queryset_list = super(ProductViewSet,self).get_queryset()
		#filter by category id
		if category:
			queryset_list = queryset_list.filter(category=category)
		if search:
			queryset_list = queryset_list.filter(
				Q(name__icontains=search)
			).distinct()

		return queryset_list


