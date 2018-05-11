from django.shortcuts import render
from .models import Order
from rest_framework import viewsets
from .serializers import OrderSerializer

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import conekta
from django.conf import settings
from decimal import Decimal

# Create your views here.
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

class Payment(APIView):
	def post(self, request, format=None):
		conekta.api_key = settings.CONEKTA_PRIVATE_KEY
		conekta.api_version = "2.0.0"
		conekta.locale = 'es'

		#usuario logueado
		user = request.user
		print(request.data)
		print(user.profile.phone)
		#orden de nuestro backend que pagaremos
		django_order = Order.objects.all().get(id=request.data['order'])
		amount = Decimal(django_order.total)

		"""Usuario en conekta"""
		# si id en profile buscamos al cliente en conekta
		if user.profile.conekta:
			try:
				customer = conekta.Customer.find(user.profile.conekta)
			except:
				pass
		else:
		# si no, lo creamos
			try:
				customer = conekta.Customer.create({
				    'name': 'Oswaldito',
				    'email': 'os@fixter.org',
				    'phone': '+52 7711732959',
				    
				    'payment_sources': [{
				      'type': 'card',
				      'token_id': 'tok_test_visa_4242'
				      #'token_id': request.data['token']['id']
				    }]
				  })
				user.profile.conekta = customer.id
				user.profile.save()
			except conekta.ConektaError as e:
				print (e)

		"""Creamos orden y pago en conekta"""
		try:
			order = conekta.Order.create({
				"line_items": [{
					"name": "Compra total",
					"unit_price": int(amount),
					"quantity": 1
				}],
				"shipping_lines": [{
					"amount": 1500,
					"carrier": "mi compañia"
				}],
				"currency": "MXN",
				"customer_info": {
					"customer_id":user.profile.conekta
				},
				"shipping_contact":{
					#"phone": "5555555555",
					#"receiver": "Bruce Wayne",
					"address": {
						"street1": "Calle 123 int 2 Col. Chida",
						"city": "Cuahutemoc",
						"state": "Ciudad de Mexico",
						"country": "MX",
						"postal_code": "06100",
						"residential": True
					}
				},
				"metadata": { "description": "Dulcecitos: 300(MXN)", "reference": "1334523452345" },
				"charges": [{
					"payment_method":{
						"type": "default",
						} 
					}]
				})
			django_order.paid = True
			django_order.save()
			serializer = OrderSerializer(django_order)
			
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		except conekta.ConektaError as e:
			order = {"payment_status":"Falló"}
			print(order)
			print (e)
			return Response('nel', status=status.HTTP_400_BAD_REQUEST)	