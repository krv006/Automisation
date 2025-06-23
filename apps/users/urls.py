from django.urls import path

from users.views import UserListAPIView, UserRegisterCreateView, VerifyCodeApiView, LoginAPIView, ManagerCreateUserView, \
    PhoneLoginAPIView, ManagerLoginView

urlpatterns = [
    path('user', UserListAPIView.as_view(), name='user-list'),

    # todo Login-Register
    path('user-register/', UserRegisterCreateView.as_view(), name='register'),
    path('verify-code', VerifyCodeApiView.as_view(), name='verify_code'),
    path('user-login/', LoginAPIView.as_view(), name='login'),

    # todo Manager-login
    path('manager/create-user/', ManagerCreateUserView.as_view(), name='manager-create-user'),
    # path('manager/login/', PhoneLoginAPIView.as_view(), name='manager-login'),
    path('manager/login/', ManagerLoginView.as_view(), name='manager-login'),
]
