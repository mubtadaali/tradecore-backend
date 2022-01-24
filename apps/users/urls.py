from django.urls.conf import path, include
from rest_framework.routers import DefaultRouter

from apps.users.views import UserViewSet


router = DefaultRouter()
router.register('', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]
