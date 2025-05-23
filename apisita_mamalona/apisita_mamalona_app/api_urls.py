from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView, TokenVerifyView, ProfileView,
    ProductListAPIView, ProductCreateAPIView, ProductDetailAPIView,
    OrderListCreateAPIView, OrderDetailAPIView
)

urlpatterns = [
    # Autenticación
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify-token/', TokenVerifyView.as_view(), name='verify-token'),

    # Perfil
    path('profile/', ProfileView.as_view(), name='profile'),

    # Productos
    path('productos/', ProductListAPIView.as_view(), name='lista-productos'),
    path('productos/crear/', ProductCreateAPIView.as_view(), name='crear-producto'),
    path('productos/<int:pk>/', ProductDetailAPIView.as_view(), name='detalle-producto'),

    # Órdenes
    path('ordenes/', OrderListCreateAPIView.as_view(), name='lista-creacion-orden'),
    path('ordenes/<int:pk>/', OrderDetailAPIView.as_view(), name='detalle-orden'),
]
