from django.contrib import admin
from django.contrib.auth import get_user_model

from db.models import UserActiveType

User = get_user_model()

admin.site.register(UserActiveType)
admin.site.register(User)