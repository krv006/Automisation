import random
import string

from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, EmailField, SerializerMethodField
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from users.gen_code import generate_code
from users.models import User
from users.task import send_verification_email


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserDetailModelSerializer(ModelSerializer):
    assigned_projects = SerializerMethodField()

    class Meta:
        model = User
        fields = 'id', 'role', 'phone_number', 'email', 'user_type', 'assigned_projects', 'full_name',

    def get_assigned_projects(self, obj):
        from project.serializers import ProjectDetailModelSerializer
        project_users = obj.assigned_projects.select_related('project')
        return [ProjectDetailModelSerializer(pu.project).data for pu in project_users]


class RegisterUserModelSerializer(ModelSerializer):
    confirm_password = CharField(write_only=True)

    class Meta:
        model = User
        fields = 'id', 'email', 'phone_number', 'first_name', 'last_name', 'password', 'confirm_password',

        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        confirm_password = attrs.pop('confirm_password')
        password = attrs.get('password')
        if confirm_password != password:
            raise ValidationError('Passwords did not match!')
        attrs['password'] = make_password(password)
        if not attrs.get('username'):
            attrs['username'] = attrs.get('email')
        return attrs

    def create(self, validated_data):
        user = super().create(validated_data)
        code = generate_code()
        cache.set(f"{user.email}_verification", code, timeout=120)
        send_verification_email.delay(user.email, code)
        return user


class LoginUserModelSerializer(Serializer):
    email = EmailField()
    password = CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("Bunday email mavjud emas bizda")

        if not user.check_password(password):
            raise ValidationError("Password ni xato kiritdingiz !!!")
        if not user.is_active:
            user.is_active = True
            user.save(update_fields=['is_active'])
        attrs['user'] = user
        return attrs


class VerifyCodeSerializer(Serializer):
    email = EmailField()
    code = CharField(write_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        email = attrs.get('email')
        code = attrs.pop('code')
        gen_code = cache.get(f'{email}_verification')
        if gen_code is None:
            raise ValidationError("Your verification already expired!")
        if code != gen_code:
            raise ValidationError("Code didn't matched")
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()
        return user


class ManagerCreateUserSerializer(ModelSerializer):
    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ('role', 'first_name', 'last_name', 'email', 'phone_number', 'password', 'user_type')
        extra_kwargs = {
            'role': {'read_only': True},
            'email': {'required': True},
            'phone_number': {'required': True},
            'password': {'required': True},
            'user_type': {'required': False}
        }

    def create(self, validated_data):
        validated_data['role'] = 'user'
        password = validated_data.pop('password')

        username = 'user_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

        user = User.objects.create_user(
            username=username,
            email=validated_data.get('email'),
            phone_number=validated_data.get('phone_number'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            password=password,
            user_type=validated_data.get('user_type')  # ✅ Bazaga yoziladi
        )
        user.is_active = True
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        password = attrs.get("password")

        if not phone_number or not password:
            raise ValidationError("Telefon raqam va parol to‘ldirilishi shart.")

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise ValidationError("Login yoki parol noto‘g‘ri.")

        if not user.check_password(password):
            raise ValidationError("Login yoki parol noto‘g‘ri.")

        if not user.is_active:
            raise ValidationError("Foydalanuvchi aktivlashtirilmagan.")

        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "role": user.role,
                "email": user.email,
                "phone_number": user.phone_number,
                "user_type": user.user_type or None
            }
        }


class PhoneLoginSerializer(Serializer):
    phone_number = CharField()
    password = CharField()

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        password = attrs.get("password")

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise ValidationError("Raqam yoki parol noto‘g‘ri.")

        if not user.check_password(password):
            raise ValidationError("Parol noto‘g‘ri.")

        if not user.is_active:
            raise ValidationError("Foydalanuvchi aktiv emas.")

        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.id,
                "email": user.email,
                "phone_number": user.phone_number,
                "role": user.role,
                "user_type": user.user_type
            }
        }
