from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'telegram_chat_id')

    def create(self, validated_data):
        user = User(username=validated_data['username'], telegram_chat_id=validated_data['telegram_chat_id'])
        user.set_password(validated_data['password'])
        user.save()
        return user
