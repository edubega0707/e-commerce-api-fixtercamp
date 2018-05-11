from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver
from products.models import Product

class Profile(models.Model):
	user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
	phone = models.IntegerField(blank=True, null=True)
	address = models.TextField(blank=True, null=True)
	conekta = models.CharField(max_length=200, blank=True, null=True)

	def __str__(self):
		return self.user.username

	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()

class UserCart(models.Model):
	user = user = models.OneToOneField(User, related_name='cart', on_delete=models.CASCADE)

	def __str__(self):
		return self.user.username

class ItemCart(models.Model):
	cart = models.ForeignKey(UserCart, related_name="items", on_delete=models.SET_NULL, blank=True, null=True)
	product = models.ForeignKey(Product, related_name="cart_items", on_delete=models.SET_NULL, blank=True, null=True)
	quantity = models.IntegerField()
	
	def __str__(self):
		return 'item {} of order {}'.format(self.product.name, self.order.id)