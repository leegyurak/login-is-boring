import random
import string

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, User
)
from django.db import models
from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import RefreshToken


class UserActiveType(models.Model):
    class TYPES(models.IntegerChoices):
        DEACTIVE = 1
        ACTIVE = 2
        SECESSION = 3

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, help_text='권한명')
    description = models.CharField(max_length=511, help_text='권한에 대한 설명')

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(
        self, 
        username: str, 
        email: str, 
        password: str, 
        nickname: str | None = None
    ) -> User:
        """
        유저를 생성하는 함수.
        """
        verify_code = ''.join(random.choices(string.digits, k=6))
        user = self.model(
            username=username,
            email=email,
            nickname=nickname,
            verify_code=verify_code
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
        self, 
        email: str, 
        password: str, 
        username: str, 
        nickname: str | None = None
    ) -> User:
        """
        어드민 유저를 생성하는 함수.
        """
        user = self.create_user(
            email=email,
            password=password,
            username=username,
            nickname=nickname
        )

        user.is_staff = True
        user.active_type = UserActiveType.objects.get(id=2)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    id = models.BigAutoField(primary_key=True)
    email = models.CharField(max_length=255, unique=True, help_text='이메일')
    username = models.CharField(max_length=255, help_text='사용자 이름')
    nickname = models.CharField(max_length=255, null=True, help_text='사용자 별명')
    active_type = models.ForeignKey(UserActiveType, default=1, on_delete=models.DO_NOTHING, help_text='사용자 활성화 여부')
    verify_code = models.CharField(max_length=127, null=True, help_text='사용자 인증 코드 (예: 비밀번호 초기화 인증, 이메일 인증)')
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_token(self) -> dict[str, str]:
        """
        유저 정보를 받아 엑세스 토큰 및 리프레시 토큰을 return하는 함수.
        """
        token = RefreshToken.for_user(self)
        access_token_expiration = (datetime.now() + timedelta(hours=4)).isoformat()
        refresh_token_expiration = (datetime.now() + timedelta(days=7)).isoformat()

        data = {
            'access_token': str(token.access_token),
            'access_token_expiration': access_token_expiration,
            'refresh_token': str(token),
            'refresh_token_expiration': refresh_token_expiration
        }

        return data