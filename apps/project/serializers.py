from rest_framework.serializers import ModelSerializer

from project.models import Project, ProjectUser
from users.serializers import UserDetailModelSerializer


class ProjectModelSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = 'id', 'name', 'description', 'created_by', 'manager',

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['created_by'] = UserDetailModelSerializer(instance.created_by).data
        repr['manager'] = UserDetailModelSerializer(instance.manager).data
        return repr


class ProjectUserModelSerializer(ModelSerializer):
    class Meta:
        model = ProjectUser
        fields = 'id', 'project', 'assigned_by',
