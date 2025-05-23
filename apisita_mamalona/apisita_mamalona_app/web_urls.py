from django.urls import re_path
from . import views

urlpatterns = [
    # Autenticación
    re_path(r'^login$', views.LoginView.as_view(), name='login'),
    re_path(r'^logout$', views.LogoutView.as_view(), name='logout'),
    re_path(r'^register$', views.RegisterView.as_view(), name='register'),
    re_path(r'^verify-token$', views.TokenVerifyView.as_view(), name='verify-token'),

    # Perfil
    re_path(r'^profile$', views.ProfileView.as_view(), name='profile'),

    # Productos
    re_path(r'^productos$', views.ProductListAPIView.as_view(), name='lista-productos'),
    re_path(r'^productos/crear$', views.ProductCreateAPIView.as_view(), name='crear-producto'),
    re_path(r'^productos/(?P<pk>\d+)$', views.ProductDetailAPIView.as_view(), name='detalle-producto'),

    # Órdenes
    re_path(r'^ordenes$', views.OrderListCreateAPIView.as_view(), name='lista-creacion-orden'),
    re_path(r'^ordenes/(?P<pk>\d+)$', views.OrderDetailAPIView.as_view(), name='detalle-orden'),
]