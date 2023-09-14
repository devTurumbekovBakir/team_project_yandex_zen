from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register('user', views.UserListCreateRetrieveUpdateDestroyAPIViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', obtain_auth_token),
]
