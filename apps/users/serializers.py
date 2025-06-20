import random
import string

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, EmailField
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.gen_code import generate_code
from users.models import User
from users.task import send_verification_email


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


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
    password = CharField(read_only=True)

    class Meta:
        model = User
        fields = ('role', 'first_name', 'last_name', 'email', 'phone_number', 'password')
        extra_kwargs = {
            'role': {'read_only': True},
            'phone_number': {'required': True},  # majburiy qilib qo‘yamiz
        }

    def create(self, validated_data):
        validated_data['role'] = 'user'

        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        user = User.objects.create_user(
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            email=validated_data.get('email', None),
            phone_number=validated_data.get('phone_number'),
            password=password
        )
        user.is_active = True
        user.save()

        user._generated_password = password
        return user

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['password'] = getattr(instance, '_generated_password', None)
        return data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError("Login yoki parol noto‘g‘ri.")

        data = super().validate(attrs)
        data['role'] = user.role
        data['email'] = user.email
        data['phone_number'] = user.phone_number
        return data
