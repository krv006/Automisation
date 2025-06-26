from django.urls import path

from project.views import ProjectListCreateAPIView, ProjectUserListCreateAPIView

urlpatterns = [
    # todo Project API
    path('project-list/', ProjectListCreateAPIView.as_view(), name='project-list'),
    path('project-user/', ProjectUserListCreateAPIView.as_view(), name='project-user'),

]
