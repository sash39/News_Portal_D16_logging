from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from datetime import datetime
from django.core.cache import cache


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, blank=True)

    @property
    def rating_author(self):
        return self.rating

    @rating_author.setter
    def rating_author(self, value):
        self.rating = int(value) if value >= 0 else 0
        self.save()

    def update_rating(self):
        self.rating = 0
        self.comment_rating = 0
        self.post_rating = 0
        self.total_comment_post = 0
        for com_iter in Comment.objects.filter(comment_user=self.user):
            self.comment_rating = self.comment_rating + com_iter.comment_rating
        for post_iter in Post.objects.filter(author=self):
            self.post_rating = self.post_rating + post_iter.post_rating
            for com_iter in Comment.objects.filter(comment_post=post_iter):
                self.total_comment_post = self.total_comment_post + com_iter.comment_rating
        self.rating = (self.post_rating * 3) + self.comment_rating + self.total_comment_post
        self.save()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return self.category_name

class Post(models.Model):
    news = 'news'
    articles = 'articles'

    CHOICES = [
        (news, 'Новости'),
        (articles, 'Статьи')
    ]

    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    text = models.TextField()
    choice = models.CharField(max_length=10, choices=CHOICES, default=articles)
    posting_time = models.DateTimeField(null=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    post_rating = models.IntegerField(default=0)

    @property
    def rating_post(self):
        return self.post_rating

    @rating_post.setter
    def rating_post(self, value):
        self.post_rating = int(value) if value >= 0 else 0
        self.save()

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:124]}...'

    def get_absolute_url(self):
        return f'/posts/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')

class PostCategory(models.Model):
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category.category_name} : {self.post.id}'


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(null=False)
    comment_date = models.DateTimeField(null=True)
    comment_rating = models.IntegerField(default=0)

    @property
    def rating_comment(self):
        return self.comment_rating

    @rating_comment.setter
    def rating_comment(self, value):
        self.comment_rating = int(value) if value >= 0 else 0
        self.save()

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

class Appointment(models.Model):
    date = models.DateField(
        default=datetime.utcnow,
    )
    client_name = models.CharField(
        max_length=200
    )
    message = models.TextField()

    def __str__(self):
        return f'{self.client_name}: {self.message}'
