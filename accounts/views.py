from django.shortcuts import render
from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework import viewsets
from .models import UserCart
from rest_framework.views import APIView
from rest_framework.response import Response




class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer 
	
class MyUser(APIView):
	
	def get(self, request, format=None):
		my_user = User.objects.all().get(id=request.user.id)
		serializer = UserSerializer(my_user)
		
		return Response(serializer.data)

