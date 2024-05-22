from django.urls import path,include

from user.views import RegisterView, LoginView, UserView, LogoutView, VerifyCodeView, ForgetPasswordView, \
     ChangePasswordView , ActivateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register' ) ,
    path('login/', LoginView.as_view(), name='login' ) ,
    path('list/' , UserView.as_view() , name='list') ,
    path('logout/', LogoutView.as_view(), name='logout') ,
    path('verify/', VerifyCodeView.as_view(), name='verify'),
    path('forgetpassword/', ForgetPasswordView.as_view(), name='forgetpassword'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('users/', UserView.as_view(), name='users'),
    path('activate/' , ActivateView.as_view(), name='activate')
]