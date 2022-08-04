from django.db import transaction
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from v1.accounts.serializers import SignUpSerializer
from v1.accounts.tasks import task_send_sign_up_verify_code_email


class SignUpView(GenericAPIView):
    serializer_class = SignUpSerializer

    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        task_send_sign_up_verify_code_email.delay(serializer.data)
        return Response({'detail': 'check your email'}, status=status.HTTP_201_CREATED)