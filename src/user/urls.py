'''
URL mapping for user API
'''
from django.urls import path
from user import views


app_name = 'user'
urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]