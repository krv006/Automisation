from django.urls import path

from users.views import UserListAPIView, UserRegisterCreateView, VerifyCodeApiView, LoginAPIView, ManagerCreateUserView, \
    ManagerLoginView, PhoneLoginAPIView, UserDetailListAPIView

urlpatterns = [
    path('user/', UserListAPIView.as_view(), name='user-list'),
    path('user-detail/', UserDetailListAPIView.as_view(), name='user-detail-list'),

    # todo Login-Register
    path('user-register/', UserRegisterCreateView.as_view(), name='register'),
    path('verify-code', VerifyCodeApiView.as_view(), name='verify_code'),
    path('user-login/', LoginAPIView.as_view(), name='login'),

    # todo Manager-login
    path('manager/create-user/', ManagerCreateUserView.as_view(), name='manager-create-user'),
    path('manager/login/email/', ManagerLoginView.as_view(), name='manager-login'),
    path('manager/login/phone/', PhoneLoginAPIView.as_view(), name='phone_login')

]
