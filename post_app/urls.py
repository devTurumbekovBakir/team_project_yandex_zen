from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.post_list_create_api_view),
    path('post/<int:pk>/', views.PostRetrieveUpdateDestroyAPIView.as_view()),
    path('post/rating/', views.RatingListCreateAPIView.as_view()),
]
