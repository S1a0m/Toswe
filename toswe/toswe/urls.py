from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from users.views import UserViewSet

router = routers.SimpleRouter()

router.register('user', UserViewSet, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
## path('tw-api/', include('rest_framework.urls')),