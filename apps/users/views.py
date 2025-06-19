from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import UserModelSerializer, RegisterUserModelSerializer, LoginUserModelSerializer, \
    VerifyCodeSerializer


@extend_schema(tags=['Auth'], description="""
API for verify code
""")
class UserRegisterCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserModelSerializer
    permission_classes = AllowAny,


@extend_schema(tags=['Auth'], description="""
API for verify code
""")
class LoginAPIView(GenericAPIView):
    serializer_class = LoginUserModelSerializer
    permission_classes = AllowAny,
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


@extend_schema(tags=['Auth'], description="""
API for verify code
""")
class VerifyCodeApiView(GenericAPIView):
    serializer_class = VerifyCodeSerializer
    queryset = User.objects.all()
    permission_classes = AllowAny,

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "Successfully verified code!"}, status=HTTP_200_OK)


@extend_schema(tags=["users"])
class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
