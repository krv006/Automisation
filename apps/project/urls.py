from django.urls import path
from rest_framework.routers import DefaultRouter

from project.views import ProjectListCreateAPIView, ProjectUserListCreateAPIView, ProjectUserRestrictedViewSet, \
    ProductListCreateAPIView, CategoryListCreateAPIView

router = DefaultRouter()
router.register('project-user', ProjectUserRestrictedViewSet, basename='project-user1')

urlpatterns = [
    # todo Project API
    path('project-list/', ProjectListCreateAPIView.as_view(), name='project-list'),
    path('project-user/', ProjectUserListCreateAPIView.as_view(), name='project-user'),

    # todo product category
    path('product-list/', ProductListCreateAPIView.as_view(), name='product-list'),
    path('category-list/', CategoryListCreateAPIView.as_view(), name='category-list'),
]
urlpatterns += router.urls
