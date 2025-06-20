from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db.models import CharField, EmailField, BooleanField, Model, DateTimeField, CASCADE, ForeignKey
from django.utils import timezone

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
    phone_number = CharField(max_length=15, blank=True, null=True)
    date_joined = DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email} - {self.username}'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'


class Manager(Model):
    user = ForeignKey('users.User', CASCADE, related_name='manager_profile')

    # todo shared model yozish kere
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.user.role != 'manager':
            raise ValidationError("Faqatgina 'manager' roliga ega foydalanuvchi Manager bo'lishi mumkin.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Manager: {self.user.full_name()} ({self.user.email})"
