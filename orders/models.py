from django.db import models
import uuid
from django.contrib.auth.models import User
from products.models import Product

# Create your models here.

class Order(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    total = models.DecimalField(decimal_places=2, max_digits=10)
    user = models.ForeignKey(User, related_name="orders", on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return 'order {} of user {}'.format(self.id, self.user.username)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, related_name="order_items", on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return 'item {} of order {}'.format(self.product.name, self.order.id)
        #return self.id

    
