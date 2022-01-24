from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from apps.posts.models import Post, Comment, Sentiment


class SentimentInline(GenericTabularInline):
    model = Sentiment
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = [SentimentInline]


class CommentAdmin(admin.ModelAdmin):
    inlines = [SentimentInline]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
