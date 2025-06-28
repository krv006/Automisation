from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from project.models import Project, ProjectUser, Category, Product


class ProjectModelSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = 'id', 'name', 'description', 'created_by', 'manager',

    def to_representation(self, instance):
        from users.serializers import UserDetailModelSerializer

        repr = super().to_representation(instance)
        repr['created_by'] = UserDetailModelSerializer(instance.created_by).data
        repr['manager'] = UserDetailModelSerializer(instance.manager).data
        return repr


class ProjectDetailModelSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description')


class ProjectUserModelSerializer(ModelSerializer):
    project = SerializerMethodField()
    assigned_by = SerializerMethodField()
    user = SerializerMethodField()

    class Meta:
        model = ProjectUser
        fields = ('id', 'project', 'assigned_by', 'user', 'progress', 'assigned_by')

    def get_project(self, instance):
        return ProjectDetailModelSerializer(instance.project).data

    def get_assigned_by(self, instance):
        from users.serializers import UserDetailModelSerializer
        return UserDetailModelSerializer(instance.assigned_by).data

    # todo buni oylab korish kerak boladi
    # def get_user(self, instance):
    #     from users.serializers import UserDetailModelSerializer
    #     return UserDetailModelSerializer(instance.user).data


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ProductModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'category')

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['category'] = CategoryModelSerializer(instance.category).data
        return repr
