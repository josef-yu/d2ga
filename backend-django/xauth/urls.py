from django.urls import path, include
from djoser.views import SetPasswordView, PasswordResetConfirmView, PasswordResetView
from . import views

urlpatterns = [
    path('password/', SetPasswordView.as_view(), name='set_password'),
    path(
        'password/reset/confirm/<uid>/<token>/', views.password_reset_confirm
    ),
    path(
        'password/reset/confirm/',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'password/reset/confirm/success/',
        views.password_reset_confirm_success,
        name='password_reset_confirm_success',
    ),
    path('', include('djoser.urls.authtoken')),
    path('password/reset/', PasswordResetView.as_view(), name="password_reset")
]