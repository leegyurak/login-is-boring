from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from v1.accounts.serializers import (
    SignUpSerializer, EmailVerifySerializer, LoginSerializer, TokenRefreshSerializer
)
from v1.accounts.tasks import task_send_sign_up_verify_code_email


User = get_user_model()


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        tags=['sign-up'],
        operation_summary='회원가입',
        responses={
            201: '회원가입 성공.',
            400: '잘못된 데이터. (형식에 맞지 않거나 중복된 데이터)'
        }
    )
)
class SignUpView(GenericAPIView):
    serializer_class = SignUpSerializer

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        """
        회원가입 기능 API.\n회원가입에 성공하면 인증코드가 담긴 이메일을 전송해준다.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        task_send_sign_up_verify_code_email.delay(serializer.data)
        return Response({'detail': 'check your email'}, status=status.HTTP_201_CREATED)


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        tags=['sign-up'],
        operation_summary='이메일 인증',
        responses={
            200: '이메일 인증 성공.',
            400: '잘못된 데이터. (형식에 맞지 않거나 중복된 데이터)',
            404: '해당하는 계정 정보를 찾을 수 없음.'
        }
    )
)
class EmailVerifyView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = EmailVerifySerializer
    filterset_fields = ('email',)

    def get_queryset(self):
        queryset = self.filter_queryset(super().get_queryset())
        
        return queryset

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        """
        이메일 인증 API.\n
        이메일로 전송된 코드를 body에 담아 전송한다.\n
        이때 이메일은 query param으로 넘긴다.
        """
        qs = self.get_queryset()
        
        if not qs.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        user = qs.first()

        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'success to verfiy'}, status=status.HTTP_200_OK)


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        tags=['login'],
        operation_summary='로그인',
        responses={
            200: '로그인 성공.',
            400: '잘못된 데이터. (형식에 맞지 않거나 중복된 데이터)',
            401: '인증되지 않은 유저. (잘못된 비밀번호 및 이메일 미인증 유저)',
            404: '해당하는 계정 정보를 찾을 수 없음.'
        }
    )
)
class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    @transaction.atomic() # exception 발생시 blacklist에 refresh token이 기록되지 않게하기 위함.
    def post(self, request, *args, **kwargs):
        """
        로그인 API.\n
        이메일과 비밀번호를 body에 담아 전송하면,
        response로 access token, refresh token 그리고 각 토큰의 만료일을 넘겨준다.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


@method_decorator(
    name='post',
    decorator=swagger_auto_schema(
        tags=['login'],
        operation_summary='엑세스 토큰 재발급',
        responses={
            200: '로그인 성공.',
            400: '잘못된 데이터. (형식에 맞지 않거나 중복된 데이터)',
            401: '잘못된 토큰'
        }
    )
)
class TokenRefreshView(GenericAPIView):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        """
        토큰 리프레시 API.\n
        유저의 리프레시 토큰을 body에 담아 전송하면,
        새로운 access token과 그 만료일을 넘겨준다. 
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data, status=status.HTTP_200_OK)