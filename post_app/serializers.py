from rest_framework import serializers

from .models import Rating, Post, Comment


class PostSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField()

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['user', 'avg_rating']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('rating', 'post',)
        read_only_fields = ['user']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['user']
