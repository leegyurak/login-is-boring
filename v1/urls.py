from django.urls import include, path


urlpatterns = [
    path('accounts/', include('v1.accounts.urls')),
]