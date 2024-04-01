from django.urls import path,include

from user.views import RegisterView , LoginView , UserView , LogoutView,VerifyCodeView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register' ) ,
    path('login/', LoginView.as_view(), name='login' ) ,
    path('list/' , UserView.as_view() , name='list') ,
    path('logout/', LogoutView.as_view(), name='logout') ,
    path('verify/', VerifyCodeView.as_view(), name='verify')
]