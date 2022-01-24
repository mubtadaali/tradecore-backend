from django.urls.conf import path, include
from rest_framework.routers import DefaultRouter

from apps.posts.views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register('', PostViewSet, basename='posts')
router.register('(?P<post_id>\\d+)/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('', include(router.urls)),
]
