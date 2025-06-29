from django.db.models import CharField, ForeignKey, CASCADE, DateTimeField
from django.db.models import Model
from django.db.models import Model
from django.db.models import Model
from django.db.models import Q


class Client(Model):
    full_name = CharField(max_length=100)
    phone = CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.full_name

class Category(Model):
    name = CharField(max_length=120)

    def __str__(self):
        return self.name


class Product(Model):
    name = CharField(max_length=120)
    category = ForeignKey('project.Category', CASCADE, related_name='products')

    def __str__(self):
        return f"{self.category}->{self.name}"


class Order(Model):
    user = ForeignKey('user.User', CASCADE, related_name='orders',
                      limit_choices_to=lambda: Q(role='Manager') | Q(role='Admin')
                      )
    order_type = CharField(max_length=50)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.email}"

# TODO shu model ga qarab ishlash kerak (Rasul aka chrome)
# https://chatgpt.com/c/6860fbea-4c94-800b-b3bb-d3d16257290b