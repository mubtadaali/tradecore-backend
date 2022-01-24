from rest_framework import serializers

from apps.posts.models import Post, Comment


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['text', 'author']


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'text', 'author', 'is_active', 'likes', 'dislikes',
            'comments_count', 'created_at', 'updated_at'
        ]
        read_only_fields = (
            'id', 'author', 'is_active', 'likes', 'dislikes',
            'comments_count', 'created_at', 'updated_at'
        )

    @staticmethod
    def get_comments_count(obj):
        return obj.comment_count

    @staticmethod
    def get_likes(obj):
        return obj.like_count

    @staticmethod
    def get_dislikes(obj):
        return obj.dislike_count


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text', 'post', 'author']


class CommentSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('text', 'post', 'author', 'likes', 'dislikes', 'created_at', 'updated_at')
        read_only_fields = ('post', 'author', 'likes', 'dislikes', 'created_at', 'updated_at')

    @staticmethod
    def get_likes(obj):
        return obj.like_count

    @staticmethod
    def get_dislikes(obj):
        return obj.dislike_count
