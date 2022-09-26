from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from v1.accounts.serializers import SignUpSerializer, EmailVerifySerializer
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

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        """
        이메일 인증 API.\n
        이메일로 전송된 코드를 body에 담아 전송한다.\n
        이때 이메일은 query param으로 넘긴다.
        """
        qs = self.filter_queryset(super().get_queryset())
        
        if not qs.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        user = qs.first()

        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'success to verfiy'}, status=status.HTTP_200_OK)