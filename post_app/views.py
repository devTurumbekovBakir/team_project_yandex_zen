from django.db.models import Avg
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import status
from .models import Post, Rating
from .permissions import PostPermission
from .serializers import PostSerializer, RatingSerializer

import requests

from datetime import datetime

BOT_TOKEN = '6264669215:AAGFx6-MSBIeM-jatCmcPLTc1a7_oU2ohT0'


def telegram_bot_sendtext(bot_token, bot_chatID, bot_message):
    send_text = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&parse_mode=Markdown&text={bot_message}'
    response = requests.get(send_text)
    return response.json()


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def post_list_create_api_view(request):
    if request.method == 'GET':
        posts = Post.objects.all().select_related('user').annotate(avg_rating=Avg('rating__rating'))
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        if request.auth.user != request.user:
            return Response({"detail": "Вы не можете создать пост с токеном другого пользователя."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)

            post_title = serializer.validated_data.get('title')
            post_body = serializer.validated_data.get('body')
            post_created = datetime.today().strftime('%Y-%m-%d %H:%M')
            telegram_message = f"Пост с названием '{post_title}' и текстом '{post_body}' успешно создан {post_created}"

            telegram_bot_sendtext(BOT_TOKEN, request.user.telegram_id, telegram_message)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all().select_related('user').annotate(avg_rating=Avg('rating__rating'))
    serializer_class = PostSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [PostPermission]


class RatingListCreateAPIView(ListCreateAPIView):
    queryset = Rating.objects.all().select_related('post').select_related('user')
    serializer_class = RatingSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [PostPermission]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
