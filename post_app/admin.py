from django.contrib import admin

from .models import Post, Rating, Comment

admin.site.register(Post)
admin.site.register(Rating)
admin.site.register(Comment)
