from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

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

@extend_schema(tags=['Project Api '], description="""
Project create 
""")
class ProjectUserRestrictedViewSet(ModelViewSet):
    queryset = ProjectUser.objects.all()
    serializer_class = ProjectUserModelSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'patch', 'delete']

    def get_queryset(self):
        user = self.request.user

        if user.role in ['admin', 'manager']:
            return ProjectUser.objects.all()

        return ProjectUser.objects.filter(user=user)

    @action(detail=True, methods=['patch'], url_path='update-progress')
    def update_progress(self, request, pk=None):
        project_user = self.get_object()

        if request.user != project_user.user:
            return Response(
                {"detail": "Siz faqat o‘zingizga biriktirilgan progress'ni o‘zgartira olasiz."},
                status=status.HTTP_403_FORBIDDEN
            )

        progress = request.data.get("progress")

        try:
            progress = int(progress)
            if not (0 <= progress <= 100):
                raise ValueError
        except (TypeError, ValueError):
            return Response(
                {"detail": "Progress qiymati 0 dan 100 gacha bo‘lishi kerak."},
                status=status.HTTP_400_BAD_REQUEST
            )

        project_user.progress = progress

        try:
            project_user.full_clean()
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        project_user.save()

        return Response({
            "detail": "Progress muvaffaqiyatli yangilandi.",
            "progress": project_user.progress
        })
