from django.contrib import admin
from .models import Profile, UserCart, ItemCart


admin.site.register(Profile)
admin.site.register(UserCart)
admin.site.register(ItemCart)

# Register your models here.
