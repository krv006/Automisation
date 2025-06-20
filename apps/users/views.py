from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers import UserModelSerializer, RegisterUserModelSerializer, LoginUserModelSerializer, \
    VerifyCodeSerializer, ManagerCreateUserSerializer, CustomTokenObtainPairSerializer


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


@extend_schema(tags=["manager-login"])
class ManagerCreateUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'manager':
            return Response({"detail": "Faqat managerlar user yaratishi mumkin."}, status=403)

        serializer = ManagerCreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


@extend_schema(tags=["manager-login"])
class ManagerLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
