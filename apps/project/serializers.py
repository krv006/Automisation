from rest_framework.serializers import ModelSerializer

from project.models import Project, ProjectUser


class ProjectModelSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = 'id', 'name', 'description', 'created_by', 'manager',


class ProjectUserModelSerializer(ModelSerializer):
    class Meta:
        model = ProjectUser
        fields = 'id', 'project', 'assigned_by',

