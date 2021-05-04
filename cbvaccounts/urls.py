from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('register/', views.RegisterPage.as_view(), name="register"),
    path('login/', views.LoginPage.as_view(), name="login"),
    path('logout/', views.LogoutUser.as_view(), name="logout"),

    path('accountsettings/', views.AccountSettings.as_view(), name="accountsettings"),

    path('', views.Home.as_view(), name="home"),
    path('user/', views.UserPage.as_view(), name="user-page"),
    path('products/', views.Products.as_view(), name="products"),
    path('customer/<str:pk>/', views.CustomerPage.as_view(), name="customer"),

    path('create_order/<str:pk>/', views.CreateOrder.as_view(), name="create_order"),
    path('update_order/<str:pk>/', views.UpdateOrder.as_view(), name="update_order"),
    path('delete_order/<str:pk>/', views.DeleteOrder.as_view(), name="delete_order"),

    path('reset_password/', 
    auth_views.PasswordResetView.as_view(template_name="cbvaccounts/password_reset.html"), 
    name="reset_password"),
    path('reset_password_sent/', 
    auth_views.PasswordResetDoneView.as_view(template_name="cbvaccounts/password_reset_sent.html"), 
    name="password_reset_done"),
    path('reset/<uidb64>/<token>/', 
    auth_views.PasswordResetConfirmView.as_view(template_name="cbvaccounts/password_reset_form.html"), 
    name="password_reset_confirm"),
    path('reset_password_complete/', 
    auth_views.PasswordResetCompleteView.as_view(template_name="cbvaccounts/password_reset_done.html"), 
    name="password_reset_complete"),
]
