from .models import Profile, ItemCart, UserCart
from django.contrib.auth.models import User
from rest_framework import serializers
from products.models import Product
from orders.serializers import OrderSerializer

class ProfileSerializer(serializers.ModelSerializer):
	#user = BasicUserSerializer(many=False, read_only=True)
	class Meta:
		model = Profile
		fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
	orders = OrderSerializer(many=True, read_only=True)
	profile = ProfileSerializer(many=False, read_only=True)
	password = serializers.CharField(write_only=True)
	class Meta:
		model = User
		fields = ['username', 'email', 'id', 'password', 'orders', 'profile']
	def create(self, validated_data):
		password = validated_data.pop('password')
		user = User.objects.create(**validated_data)
		user.set_password(password)
		user.save()

		return user

