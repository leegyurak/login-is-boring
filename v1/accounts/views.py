from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from v1.accounts.serializers import SignUpSerializer


class SignUpView(GenericAPIView):
    serializer_class = SignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)