from django.urls import path
from rest_framework.permissions import AllowAny

from users.apps import UsersConfig
from users.views import UserRetrieveUpdateAPIView, UserListAPIView, UserCreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


app_name = UsersConfig.name





urlpatterns = [
    path("users/<int:pk>/retrieve_update/", UserRetrieveUpdateAPIView.as_view(), name="users_retrieve_update"),
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),

    # path("users/create/", UserCreateAPIView.as_view(), name="users_create"),
    # path("users/<int:pk>/delete/", UserDestroyAPIView.as_view(), name="users_delete"),
    path("users/", UserListAPIView.as_view(), name="users"),
]
