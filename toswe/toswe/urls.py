from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from django.conf import settings
from django.conf.urls.static import static

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

from products.views import ProductViewSet, CartViewSet, OrderViewSet, DeliveryViewSet, PaymentViewSet, FeedbackViewSet, CategoryViewSet, AdViewSet
from users.views import UserViewSet, NotificationViewSet, RefreshTokenView

router = routers.SimpleRouter()

router.register(r'user', UserViewSet, basename='user')
router.register(r'feedback', FeedbackViewSet, basename='feedback')
router.register(r'notification', NotificationViewSet, basename='notification')

router.register(r'category', CategoryViewSet, basename='category')
router.register(r'product', ProductViewSet, basename='product')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'order', OrderViewSet, basename='order')
router.register(r'delivery', DeliveryViewSet, basename='delivery')

router.register(r"ad", AdViewSet, basename="ad")
router.register(r'payment', PaymentViewSet, basename='payment')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tw-api/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('api/refresh_token/', RefreshTokenView.as_view(), name='refresh_token'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
