from django.contrib.auth import views as auth_views
from django.urls import path

from apps.users import views

urlpatterns = [
    path("accounts/", views.UserListView.as_view(), name="user_list"),
    path("accounts/<uuid:pk>/", views.UserDetailView.as_view(), name="user_detail"),
    path("accounts/profile/", views.UserEditView.as_view(), name="user_change"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("register/<uidb64>/<token>/", views.RegisterConfirmView.as_view(), name="register_confirm"),
    path("register/done/", views.RegisterDoneView.as_view(), name="register_done"),
    path("email_reset/", views.EmailResetView.as_view(), name="email_reset"),
    path("email_reset/<uidb64>/<token>/", views.EmailResetConfirmView.as_view(), name="email_reset_confirm"),
    path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("password_change/", views.PasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
