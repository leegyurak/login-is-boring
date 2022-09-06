import re

from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()

class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(help_text='이메일 입력')
    password = serializers.CharField(write_only=True, help_text='비밀번호 입력, 최소 8자, 영어 숫자 및 특수문자 한개 필수 포함.')
    active_type = serializers.CharField(read_only=True, source='active_type.name', help_text='활성화 정보')
    verify_code = serializers.CharField(read_only=True, help_text='회원 가입시 생성되는 인증 코드')

    def validate_username(self, username: str) -> str:
        """
        유저이름의 유효성을 검사.\n
        2~4자의 유효한 한글이름을 판단한다.
        """
        regex = re.compile('^[가-힣]{2,4}$')
        match_obj = regex.match(username)

        if not match_obj:
            raise serializers.ValidationError('Please enter an exact 2-4 character Korean name.')

        return username

    def validate_email(self, email: str) -> str:
        """
        이메일의 유효성을 검사.\n
        존재하는 이메일인지 아닌지를 검사한다.
        """
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('This email already exists.')

        return email

    def validate_password(self, password: str) -> str:
        """
        비밀번호의 유효성을 검사.\n
        8자리가 넘으며 영어 및 특수문자 한개 이상이 포함되었는지를 검사한다.
        """
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
        fields = ('username', 'email', 'password', 'nickname', 'active_type', 'verify_code')


class EmailVerifySerializer(serializers.Serializer):
    verify_code = serializers.CharField(help_text='회원 가입시 생성되는 인증 코드')

    def update(self, instance, validated_data):
        verify_code = validated_data['verify_code']

        if instance.active_type_id == 2:
            raise serializers.ValidationError({'detail': 'This user is already verified.'})

        if instance.verify_code == verify_code:
            instance.active_type_id = 2
            instance.verify_code = None

            instance.save(update_fields=('active_type', 'verify_code'))
        else:
            raise serializers.ValidationError({'detail': 'verify code is not correct.'})

        return instance