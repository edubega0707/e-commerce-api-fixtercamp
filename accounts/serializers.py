from .models import Profile
from django.contrib.auth.models import User
from rest_framework import serializers

class ProfileSerializer(serializers.ModelSerializer):
	#user = BasicUserSerializer(many=False, read_only=True)
	class Meta:
		model = Profile
		fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
	#profile = ProfileSerializer(many=False, read_only=True)
	password = serializers.CharField(write_only=True)
	class Meta:
		model = User
		fields = ['username', 'email', 'id', 'password']
	def create(self, validated_data):
		password = validated_data.pop('password')
		user = User.objects.create(**validated_data)
		user.set_password(password)
		user.save()

		return user