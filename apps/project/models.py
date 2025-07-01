from django.db.models import CharField, ForeignKey, CASCADE, DateTimeField, SET_NULL
from django.db.models import Model
from django.db.models import Model
from django.db.models import Model
from django.db.models import Q


# Zakazchi (buyurtma beruvchi) mijoz
class Client(Model):
    full_name = CharField(max_length=100)
    phone = CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.full_name


# Xona turlari (Yotoqxona, Oshxona va h.k.)
class Category(Model):
    name = CharField(max_length=100)

    def __str__(self):
        return self.name


# Xonaga tegishli mahsulotlar (Krovat, Shkaf va h.k.)
class Product(Model):
    name = CharField(max_length=100)
    category = ForeignKey('project.Category', CASCADE, related_name='products')

    def __str__(self):
        return f"{self.name} ({self.category.name})"


# Zakaz (buyurtma)
class Order(Model):
    client = ForeignKey('project.Client', CASCADE, related_name='orders')
    category = ForeignKey('project.Category', CASCADE)
    created_by = ForeignKey('users.User', SET_NULL, null=True, related_name='created_orders')
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.full_name} - {self.category.name}"


# Zakazdagi mahsulotlar (har bir zakazga kerakli productlar)
class OrderItem(Model):
    order = ForeignKey('project.Order', CASCADE, related_name='items')
    product = ForeignKey('project.Product', CASCADE)

    def __str__(self):
        return f"{self.order} -> {self.product.name}"


# Zakazga biriktirilgan ishchilar
class OrderAssignment(Model):
    order = ForeignKey('project.Order', CASCADE, related_name='assignments')
    worker = ForeignKey('users.User', CASCADE, limit_choices_to={'role': 'worker'})

    def __str__(self):
        return f"{self.order} -> {self.worker.username}"

# TODO shu model ga qarab ishlash kerak (Rasul aka chrome)
# https://chatgpt.com/c/6860fbea-4c94-800b-b3bb-d3d16257290b