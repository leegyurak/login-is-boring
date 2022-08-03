from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class DefaultModel(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True, help_text='생성 날짜')


class DefaultTypeModel(DefaultModel):
    name = models.CharField(max_length=255, help_text='타입 이름')
    description = models.CharField(max_length=511, help_text='타입에 대한 설명')

    def __str__(self):
        return self.name


class DefaultBaseUser(AbstractBaseUser, DefaultModel):
    pass