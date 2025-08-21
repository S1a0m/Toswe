from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from django.conf import settings
from django.conf.urls.static import static

from products.views import ProductViewSet, CartViewSet, OrderViewSet, DeliveryViewSet, PaymentViewSet
from users.views import UserViewSet, FeedbackViewSet, NotificationViewSet, RefreshTokenView, BrandViewSet

router = routers.SimpleRouter()

router.register(r'user', UserViewSet, basename='user')
router.register(r'brands', BrandViewSet, basename='brands')
router.register(r'feedback', FeedbackViewSet, basename='feedback')
router.register(r'notification', NotificationViewSet, basename='notification')

router.register(r'product', ProductViewSet, basename='product')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'order', OrderViewSet, basename='order')
router.register(r'delivery', DeliveryViewSet, basename='delivery')

router.register(r'payment', PaymentViewSet, basename='payment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tw-api/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('refresh-token/', RefreshTokenView.as_view(), name='refresh-token'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
