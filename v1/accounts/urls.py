from django.urls import path

from v1.accounts.views import (
    SignUpView, EmailVerifyView, LoginView, TokenRefreshView
)


urlpatterns = [
    path('sign-up', SignUpView.as_view()),
    path('email-verify', EmailVerifyView.as_view()),
    path('login', LoginView.as_view()),
    path('token-refresh', TokenRefreshView.as_view()),
]
