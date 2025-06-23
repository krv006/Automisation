from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField, BooleanField, Model, DateTimeField, SET_NULL, ForeignKey
from django.utils import timezone

from shared.model import TimeBaseModel
from users.managers import CustomUserManager


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('warehouseman', 'Warehouseman'),
        ('user', 'User'),
    ]
    role = CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    first_name = CharField(max_length=150, blank=True)
    last_name = CharField(max_length=150, blank=True)
    email = EmailField(unique=True)
    is_active = BooleanField(default=False)
    phone_number = CharField(max_length=15, unique=True)
    date_joined = DateTimeField(default=timezone.now)
    user_type = ForeignKey('users.UserType', SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email} - {self.username}'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

class UserType(Model):
    name = CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# class Manager(TimeBaseModel):
#     user = ForeignKey('users.User', CASCADE, related_name='manager_profile')
#
#     def clean(self):
#         if self.user.role != 'manager':
#             raise ValidationError("Faqatgina 'manager' roliga ega foydalanuvchi Manager bo'lishi mumkin.")
#
#     def save(self, *args, **kwargs):
#         self.clean()
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         return f"Manager: {self.user.full_name()} ({self.user.email})"
