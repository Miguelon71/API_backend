from django.urls import path
from .views import RegisterView, LoginView, ProfileView
from apisita_mamalona_app.views import ProductListAPIView

urlpatterns = [
    path('productos/', ProductListAPIView.as_view(), name='lista-productos'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
]