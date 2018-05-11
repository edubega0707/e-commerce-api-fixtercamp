from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from django.conf import settings
from django.views.static import serve
from rest_framework import routers
from products.views import ProductViewSet, CategoryViewSet
from accounts.views import UserViewSet, MyUser
from orders.views import OrderViewSet, Payment
from rest_framework.authtoken import views


router = routers.DefaultRouter()
router.register('products', ProductViewSet)
router.register('users', UserViewSet)
router.register('orders', OrderViewSet)
router.register('categories', CategoryViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    path('my_user/', MyUser.as_view()),
    path('pay/', Payment.as_view()),
    path('', include(router.urls)),
    url(
        regex=r'^media/(?P<path>.*)$',
        view=serve,
        kwargs={'document_root': settings.MEDIA_ROOT}
    ),
]
