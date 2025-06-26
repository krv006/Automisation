from django.core.exceptions import ValidationError
from django.db.models import Model, CharField, TextField, CASCADE, SET_NULL, ForeignKey

from shared.model import TimeBaseModel


class Project(Model):
    name = CharField(max_length=255)
    description = TextField(blank=True)
    created_by = ForeignKey('users.User', SET_NULL, null=True, related_name='created_projects')  # Admin
    manager = ForeignKey('users.User', SET_NULL, null=True, related_name='managed_projects')  # Manager

    def clean(self):
        if self.created_by and self.created_by.role != 'admin':
            raise ValidationError("Loyihani faqat 'admin' yaratishi mumkin.")
        if self.manager and self.manager.role != 'manager':
            raise ValidationError("Loyihaga faqat 'manager' roli bor foydalanuvchi biriktiriladi.")

    def __str__(self):
        return f"{self.name} (Manager: {self.manager.full_name() if self.manager else 'None'})"


class ProjectUser(Model):
    project = ForeignKey('project.Project', CASCADE, related_name='project_users')
    user = ForeignKey('users.User', CASCADE, related_name='assigned_projects')
    assigned_by = ForeignKey('users.User', SET_NULL, null=True, related_name='assigned_users')

    def clean(self):
        if self.user.role != 'user':
            raise ValidationError("Faqat 'user' roli bor foydalanuvchi projectga biriktiriladi.")
        if self.assigned_by:
            if self.assigned_by.role != 'manager':
                raise ValidationError("User'ni projectga faqat manager biriktira oladi.")
            if self.assigned_by != self.project.manager:
                raise ValidationError("User'ni faqat shu project manager'i biriktira oladi.")

    def __str__(self):
        return f"{self.project.name} → {self.user.full_name()}"
