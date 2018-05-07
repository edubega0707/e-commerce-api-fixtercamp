from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from django.conf import settings
from django.views.static import serve
from rest_framework import routers
from products.views import ProductViewSet
from accounts.views import UserViewSet
from orders.views import OrderViewSet
from rest_framework.authtoken import views


router = routers.DefaultRouter()
router.register('products', ProductViewSet)
router.register('users', UserViewSet)
router.register('orders', OrderViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls)),
    url(
        regex=r'^media/(?P<path>.*)$',
        view=serve,
        kwargs={'document_root': settings.MEDIA_ROOT}
    ),
]
