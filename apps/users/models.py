from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField, BooleanField, Model, DateTimeField, DateField
from django.utils import timezone

from users.managers import CustomUserManager


class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('warehouseman', 'Warehouseman'),
    ]
    role = CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    first_name = CharField(max_length=150, blank=True)
    last_name = CharField(max_length=150, blank=True)

    email = EmailField(unique=True)
    is_active = BooleanField(default=False)

    # todo Talaba haqida qo‘shimcha ma'lumotlar
    date_of_birth = DateField(null=True, blank=True)
    phone_number = CharField(max_length=15, blank=True, null=True)
    date_joined = DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email} - {self.username}'

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
