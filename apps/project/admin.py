from django.contrib import admin
from django.contrib.admin import ModelAdmin

from project.models import Project, ProjectUser


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    pass


@admin.register(ProjectUser)
class ProjectUserAdmin(ModelAdmin):
    pass
