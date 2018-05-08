from django.shortcuts import render
from .models import Order
from rest_framework import viewsets
from .serializers import OrderSerializer

# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
