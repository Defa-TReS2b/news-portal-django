from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, db_column="rating")

    def update_rating(self):
        self.rating = 0
        for post in self.post_set.all():
            self.rating += post.rating * 3
            for other_comment in post.comment_set.exclude(author__username=self.user.username):
                self.rating += other_comment.rating
        for comment in self.user.comment_set.all():
            self.rating += comment.rating
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=25, unique=True)


class Post(models.Model):
    NT = "NT"
    NW = "NW"

    STATES = [
        ("NT", "Заметка"),
        ("NW", "Новость"),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    state = models.CharField(max_length=2, choices=STATES, default="NT")
    datetime = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through="PostCategory")
    title = models.CharField(max_length=25)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def preview(self):
        return self.text[:123] + "..."

    def like(self, a=1):
        self.rating += a
        self.save()

    def dislike(self, a=1):
        self.rating -= a
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self, a=1):
        self.rating += a
        self.save()

    def dislike(self, a=1):
        self.rating -= a
        self.save()
