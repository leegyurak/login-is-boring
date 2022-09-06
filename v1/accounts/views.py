from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from v1.accounts.serializers import SignUpSerializer, EmailVerifySerializer
from v1.accounts.tasks import task_send_sign_up_verify_code_email


User = get_user_model()

class SignUpView(GenericAPIView):
    serializer_class = SignUpSerializer

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        task_send_sign_up_verify_code_email.delay(serializer.data)
        return Response({'detail': 'check your email'}, status=status.HTTP_201_CREATED)


class EmailVerifyView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = EmailVerifySerializer
    filterset_fields = ('email',)

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        qs = self.filter_queryset(super().get_queryset())
        
        if not qs.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        user = qs.first()

        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': 'success to verfiy'}, status=status.HTTP_200_OK)