from django.db.models import Count, Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet

from apps.posts.models import Post, Sentiment, Comment
from apps.posts.permissions import IsAuthorOrReadOnly
from apps.posts.serializers import PostSerializer, PostCreateSerializer, CommentCreateSerializer, CommentSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        return PostSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthorOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return self.queryset.annotate(
            comment_count=Count('comments'),
            like_count=Count('sentiments', filter=Q(sentiments__sentiment_type=Sentiment.LIKE)),
            dislike_count=Count('sentiments', filter=Q(sentiments__sentiment_type=Sentiment.DIS_LIKE)),
        )

    def filter_queryset(self, queryset):
        author = self.request.query_params.get('author', '')
        if author and author.isnumeric():
            queryset = queryset.filter(author=author)
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data.update({'author': request.user.id})

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    def perform_destroy(self, instance):
        instance.soft_delete()


class CommentViewSet(ModelViewSet):

    def get_serializer_class(self):
        if self.action == 'create':
            return CommentCreateSerializer
        return CommentSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data.update({
            'post': self.kwargs['post_id'],
            'author': request.user.id
        })
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        return Comment.objects.filter(
            post_id=self.kwargs['post_id']
        ).annotate(
            like_count=Count('sentiments', filter=Q(sentiments__sentiment_type=Sentiment.LIKE)),
            dislike_count=Count('sentiments', filter=Q(sentiments__sentiment_type=Sentiment.DIS_LIKE)),
        )

    def filter_queryset(self, queryset):
        author = self.request.query_params.get('author', '')
        if author and author.isnumeric():
            queryset = queryset.filter(author=author)
        return queryset

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthorOrReadOnly]
        return [permission() for permission in permission_classes]
