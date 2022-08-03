from django.urls import path

from v1.accounts.views import SignUpView


urlpatterns = [
    path('sign-up', SignUpView.as_view())
]
