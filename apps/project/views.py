from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView

from project.models import Project, ProjectUser
from project.serializers import ProjectModelSerializer, ProjectUserModelSerializer


@extend_schema(tags=['Project Api '], description="""
Project create 
""")
class ProjectListCreateAPIView(ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectModelSerializer
    # permission_classes = AllowAny,


@extend_schema(tags=['Project Api '], description="""
Project create 
""")
class ProjectUserListCreateAPIView(ListCreateAPIView):
    queryset = ProjectUser.objects.all()
    serializer_class = ProjectUserModelSerializer
    # permission_classes = AllowAny,
