from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

RATINGS = (
    (1, 'Очень плохо'),
    (2, 'Плохо'),
    (3, 'Так себе'),
    (4, 'Хорошо'),
    (5, 'Отлично')
)


class Post(models.Model):
    title = models.CharField(max_length=256)
    body = models.TextField(max_length=256)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return f'{self.title} - {self.user.username}'


class Rating(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATINGS)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
        unique_together = ('post', 'user')

    def __str__(self):
        return f'{self.post.title} ({self.user.username}): {self.rating}'


class Comment(models.Model):
    text = models.TextField(max_length=426)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.user.username} - {self.post.title}'
