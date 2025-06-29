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
    class Meta:
        model = ProjectUser
        fields = ('id', 'project', 'assigned_by', 'user', 'progress', 'assigned_by')

    def to_representation(self, instance):
        from users.serializers import UserDetailModelSerializer

        repr = super().to_representation(instance)
        repr['project'] = ProjectDetailModelSerializer(instance.project).data
        repr['user'] = UserDetailModelSerializer(instance.user).data
        repr['assigned_by'] = UserDetailModelSerializer(instance.assigned_by).data
        return repr


class CategoryModelSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = 'id', 'name',


class ProductModelSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = 'id', 'name', 'category',

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['category'] = CategoryModelSerializer(instance.category).data
        return repr
