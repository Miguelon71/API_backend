from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView, TokenVerifyView, ProfileView,
    ProductListAPIView, ProductCreateAPIView, ProductDetailAPIView,
    OrderListCreateAPIView, OrderDetailAPIView
)

urlpatterns = [
    # Autenticación
    path('register/', RegisterView.as_view(), name='api-register'),
    path('login/', LoginView.as_view(), name='api-login'),
    path('logout/', LogoutView.as_view(), name='api-logout'),
    path('verify-token/', TokenVerifyView.as_view(), name='api-verify-token'),

    # Perfil
    path('profile/', ProfileView.as_view(), name='api-profile'),

    # Productos
    path('productos/', ProductListAPIView.as_view(), name='api-lista-productos'),
    path('productos/crear/', ProductCreateAPIView.as_view(), name='api-crear-producto'),
    path('productos/<int:pk>/', ProductDetailAPIView.as_view(), name='api-detalle-producto'),

    # Órdenes
    path('ordenes/', OrderListCreateAPIView.as_view(), name='api-lista-creacion-orden'),
    path('ordenes/<int:pk>/', OrderDetailAPIView.as_view(), name='api-detalle-orden'),
]
