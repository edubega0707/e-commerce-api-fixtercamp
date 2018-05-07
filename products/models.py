from django.db import models
import uuid


class Category(models.Model):
	name = models.CharField(max_length=200, unique=True)

	def __str__(self):
		return self.name

class Product(models.Model):
	#id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=200)
	description = models.TextField()
	price = models.DecimalField(max_digits=10, decimal_places=2)
	photo = models.ImageField(upload_to="product_photos")
	in_stock = models.BooleanField(default=True)
	in_sale = models.BooleanField(default=False)
	sale_price = models.DecimalField(max_digits=10, decimal_places=2)
	category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, blank=True, null=True)
	#slug
	class Meta:
		ordering:'-id'


	def __str__(self):
		return self.name
