from django.urls import path

from users.views import UserListAPIView, UserRegisterCreateView, VerifyCodeApiView, LoginAPIView

urlpatterns = [
    path('user', UserListAPIView.as_view(), name='user-list'),

    # todo Login-Register
    path('user-register/', UserRegisterCreateView.as_view(), name='register'),
    path('verify-code', VerifyCodeApiView.as_view(), name='verify_code'),
    path('user-login/', LoginAPIView.as_view(), name='login'),
]
