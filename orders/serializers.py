from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product
import uuid
from django.db.models import UUIDField
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)
    product_id=(serializers.PrimaryKeyRelatedField(
		queryset=Product.objects.all(), 
        #pk_field=UUIDField(format='hex_verbose'),
		write_only=True, 
		required=False,
        many=False))
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)
    #items_id = serializers.PrimaryKeyRelatedField(
		# queryset=OrderItem.objects.all(), 
		# write_only=True, 
		# allow_null=True, 
		# required=False,
        # many=True)
    user = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = '__all__'
    """
    need to pass product id and quantity in an object called item in this case
    """
    def create(self, validated_data):
        print(validated_data)
        order_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for o in order_data:
            print(o)
            p = o['product_id']
            q = o['quantity']
            
            OrderItem.objects.create(order=order,quantity=q, product=p)
            
        return order