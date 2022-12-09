"""
URL mapping for user API
"""
from django.urls import path
from knox import views as knox_views
from user import views

app_name = 'user'
urlpatterns = [
    path(
        'register-by-access-token/social/google-oauth2/',
        views.LoginWithGoogle.as_view(),
        name='login_with_google'
    ),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path(
        'logout-all-device/',
        knox_views.LogoutAllView.as_view(),
        name='knox_logoutall'
    ),
]
