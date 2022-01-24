from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet

from apps.posts.models import Post, Sentiment, Comment
from apps.posts.permissions import IsAuthorOrReadOnly
from apps.posts.serializers import PostSerializer, PostCreateSerializer, CommentCreateSerializer, CommentSerializer


class SentimentModelViewSet(ModelViewSet):

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'like', 'dislike']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthorOrReadOnly]
        return [permission() for permission in permission_classes]

    def filter_queryset(self, queryset):
        author = self.request.query_params.get('author', '')
        if author and author.isnumeric():
            queryset = queryset.filter(author=author)
        return queryset

    def create_object(self, request_data):
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    @staticmethod
    def get_content_type(**kwargs):
        model = 'comment' if 'post_id' in kwargs else 'post'
        return ContentType.objects.get(app_label='posts', model=model)

    @action(detail=True, methods=['get'])
    def like(self, request, *args, **kwargs):
        Sentiment.objects.update_or_create(
            user=request.user,
            object_id=self.kwargs['pk'],
            content_type=self.get_content_type(**kwargs),
            defaults={'sentiment_type': Sentiment.LIKE}
        )
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def dislike(self, request, *args, **kwargs):
        Sentiment.objects.update_or_create(
            user=request.user,
            object_id=self.kwargs['pk'],
            content_type=self.get_content_type(**kwargs),
            defaults={'sentiment_type': Sentiment.DIS_LIKE}
        )
        return Response(status=status.HTTP_200_OK)


class PostViewSet(SentimentModelViewSet):
    queryset = Post.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == 'create':
            return PostCreateSerializer
        return PostSerializer

    def get_queryset(self):
        return self.queryset.annotate(
            comment_count=Count('comments'),
            like_count=Count('sentiments', filter=Q(sentiments__sentiment_type=Sentiment.LIKE)),
            dislike_count=Count('sentiments', filter=Q(sentiments__sentiment_type=Sentiment.DIS_LIKE)),
        )

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data.update({'author': request.user.id})
        return self.create_object(data)

    def perform_destroy(self, instance):
        instance.soft_delete()


class CommentViewSet(SentimentModelViewSet):

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
        return self.create_object(data)

    def get_queryset(self):
        return Comment.objects.filter(
            post_id=self.kwargs['post_id']
        ).annotate(
            like_count=Count('sentiments', filter=Q(sentiments__sentiment_type=Sentiment.LIKE)),
            dislike_count=Count('sentiments', filter=Q(sentiments__sentiment_type=Sentiment.DIS_LIKE)),
        )
