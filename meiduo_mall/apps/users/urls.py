# -*-coding:utf-8-*-
# @Author: DZQ 
# @Time:2025/2/26 11:29
from django.urls import path
from apps.users.views import UsernameCountView, RegisterView, LoginView, LogoutView, CenterView, EmailView, EmailVerifyView
from apps.users.views import AddressCreateView, AddressView, UpdateDestroyAddressView, DefaultAddressView, UpdateTitleAddressView
from apps.users.views import ChangePasswordView, UserHistoryView
urlpatterns = [
    # 判断用户名是否重复
    path('usernames/<username:username>/count/', UsernameCountView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('info/', CenterView.as_view()),
    path('emails/', EmailView.as_view()),
    path('emails/verification/', EmailVerifyView.as_view()),
    path('addresses/create/', AddressCreateView.as_view()),
    path('addresses/', AddressView.as_view()),
    path('addresses/<int:address_id>/', UpdateDestroyAddressView.as_view()),
    path('addresses/<int:address_id>/default/', DefaultAddressView.as_view()),
    path('addresses/<int:address_id>/title/', UpdateTitleAddressView.as_view()),
    path('password/', ChangePasswordView.as_view()),
    path('browse_histories/', UserHistoryView.as_view()),

]