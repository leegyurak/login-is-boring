import re

from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(help_text='이메일 입력')
    password = serializers.CharField(write_only=True, help_text='비밀번호 입력, 최소 8자, 영어 숫자 및 특수문자 한개 필수 포함.')
    active_type = serializers.CharField(read_only=True, source='active_type.name', help_text='활성화 정보')

    def validate_username(self, username):
        regex = re.compile('^[가-힣]{2,4}$')
        match_obj = regex.match(username)

        if not match_obj:
            raise serializers.ValidationError('Please enter an exact 2-4 character Korean name.')

        return username

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('This email already exists.')

        return email

    def validate_password(self, password):
        regex = re.compile('^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$')
        match_obj = regex.match(password)

        if not match_obj:
            raise serializers.ValidationError(
                'Password must be at least 8 characters including English and at least one special character.'
            )

        return password

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'nickname', 'active_type')