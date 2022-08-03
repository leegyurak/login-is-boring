from django.contrib.auth.models import BaseUserManager
from django.db import models

from db.common import DefaultTypeModel, DefaultBaseUser


class UserActiveType(DefaultTypeModel):
    class _TYPES(models.IntegerChoices):
        DEACTIVE = 1
        ACTIVE = 2
        SECESSION = 3


class UserManager(BaseUserManager):
    def create_user(self, username: str, email: str, password: str, nickname=None):
        user = self.model(
            username=username,
            email=email,
            nickname=nickname
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email: str, password: str, username: str, nickname=None):
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


class User(DefaultBaseUser):
    email = models.CharField(max_length=255, unique=True, help_text='이메일')
    username = models.CharField(max_length=255, help_text='사용자 이름')
    nickname = models.CharField(max_length=255, null=True, help_text='사용자 별명')
    active_type = models.ForeignKey(UserActiveType, default=1, on_delete=models.DO_NOTHING, help_text='사용자 활성화 여부')
    verify_code = models.CharField(max_length=127, null=True, help_text='사용자 인증 코드 (예: 비밀번호 초기화 인증, 이메일 인증)')
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True