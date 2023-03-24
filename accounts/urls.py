from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views


# add simplejwt urls for access and refresh tokens
urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'), 
    # register_view
    path("register_user", views.UserRegisterView.as_view(), name="register_normal_user"),

]