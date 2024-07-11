from django.urls import path

from users.apps import UsersConfig
from users.views import UserRetrieveUpdateAPIView, UserListAPIView

app_name = UsersConfig.name


urlpatterns = [
    path("users/<int:pk>/retrieve_update/", UserRetrieveUpdateAPIView.as_view(), name="users_retrieve_update"),
    # path("users/create/", UserCreateAPIView.as_view(), name="users_create"),
    # path("users/<int:pk>/delete/", UserDestroyAPIView.as_view(), name="users_delete"),
    path("users/", UserListAPIView.as_view(), name="users"),
]
