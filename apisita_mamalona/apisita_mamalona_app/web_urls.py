from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^login$', views.LoginView.as_view(), name='login'),
    re_path(r'^register$', views.RegisterView.as_view(), name='register'),
    re_path(r'^profile$', views.ProfileView.as_view(), name='profile'),
]