from django.urls import path
from rest_framework.routers import DefaultRouter

from project.views import ProjectListCreateAPIView, ProjectUserListCreateAPIView, ProjectUserRestrictedViewSet

router = DefaultRouter()
router.register('project-user', ProjectUserRestrictedViewSet, basename='project-user')

urlpatterns = [
    # todo Project API
    path('project-list/', ProjectListCreateAPIView.as_view(), name='project-list'),
    path('project-user/', ProjectUserListCreateAPIView.as_view(), name='project-user'),

]
urlpatterns += router.urls
