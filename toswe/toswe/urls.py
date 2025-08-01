from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from users.views import UserViewset

router = routers.SimpleRouter()

router.register('user', UserViewset, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
## path('tw-api/', include('rest_framework.urls')),