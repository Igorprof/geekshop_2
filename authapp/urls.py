from django.urls import path

from authapp import views as auth_views

app_name = 'authapp'

urlpatterns = [
    path('login/', auth_views.login, name='login'), 
    path('register/', auth_views.register, name='register'),
    path('logout/', auth_views.logout, name='logout'),
    path('profile/', auth_views.profile, name='profile'),
]