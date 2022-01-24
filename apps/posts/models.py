from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

from common.mixins import CreateUpdateModelMixin, SoftDeleteModelMixin


class Sentiment(models.Model):
    DIS_LIKE = 0
    LIKE = 1
    SENTIMENT_TYPES = (
        (LIKE, 'Like'),
        (DIS_LIKE, 'Dislike'),
    )
    user = models.ForeignKey(User, related_name='activities', on_delete=models.CASCADE)
    sentiment_type = models.PositiveSmallIntegerField(choices=SENTIMENT_TYPES, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self):
        return f'{self.user.username} - {self.get_sentiment_type_display()}'


class SentimentMixin(models.Model):
    sentiments = GenericRelation(Sentiment)

    class Meta:
        abstract = True

    def total_likes(self):
        return self.sentiments.filter(sentiment_type=Sentiment.LIKE).count()

    def total_dis_likes(self):
        return self.sentiments.filter(sentiment_type=Sentiment.DIS_LIKE).count()


class Post(CreateUpdateModelMixin, SoftDeleteModelMixin, SentimentMixin):
    text = models.TextField(blank=False, null=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:15]


class Comment(CreateUpdateModelMixin, SentimentMixin):
    text = models.CharField(max_length=255, null=False, blank=False)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:15]
