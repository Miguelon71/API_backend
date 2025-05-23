from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView
from rest_framework.authtoken.models import Token
from django.db import transaction

from .models import Product, Order
from .serializers import UserSerializer, ProductSerializer, OrderSerializer


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        if data.get('password') != data.get('password_confirmation'):
            return Response({'error': 'Las contraseñas no coinciden'}, status=400)

        user = User.objects.create_user(
            username=data['email'],
            email=data['email'],
            password=data['password'],
            first_name=data['name']
        )
        token = Token.objects.create(user=user)
        return Response({'message': 'Usuario registrado correctamente', 'token': token.key, 'user': UserSerializer(user).data}, status=201)


class LoginView(APIView):
    def post(self, request):
        data = request.data
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user is not None:
            #token, _ = Token.objects.get_or_create(user=user)
            #return Response({"message": "Login exitoso", "token": token.key, "user": UserSerializer(user).data})
            return Response({'message': 'Login exitoso'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        return Response({'message': 'Sesión cerrada exitosamente'})


class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class TokenVerifyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({'message': 'Token is valid.', 'user': UserSerializer(request.user).data})


class ProductListAPIView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductCreateAPIView(APIView):
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response({'message': 'Producto creado exitosamente', 'product': ProductSerializer(product).data}, status=201)
        return Response({'errors': serializer.errors}, status=422)


class ProductDetailAPIView(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        return Response({'product': ProductSerializer(product).data})

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Producto actualizado exitosamente', 'product': serializer.data})
        return Response({'errors': serializer.errors}, status=422)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orders.exists():
            return Response({'message': 'No se puede eliminar el producto porque está asociado a órdenes'}, status=409)
        product.delete()
        return Response({'message': 'Producto eliminado exitosamente'})


class OrderListCreateAPIView(APIView):
    def get(self, request):
        orders = Order.objects.prefetch_related('products').all()
        return Response(OrderSerializer(orders, many=True).data)

    def post(self, request):
        data = request.data
        with transaction.atomic():
            serializer = OrderSerializer(data=data)
            if serializer.is_valid():
                order = serializer.save()
                for item in data['products']:
                    product = Product.objects.get(id=item['id'])
                    order.products.add(product, through_defaults={'quantity': item['quantity']})
                return Response({'message': 'Orden creada exitosamente', 'order': OrderSerializer(order).data}, status=201)
            return Response(serializer.errors, status=422)


class OrderDetailAPIView(APIView):
    def get(self, request, pk):
        order = get_object_or_404(Order.objects.prefetch_related('products'), pk=pk)
        return Response({'order': OrderSerializer(order).data})

    def put(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        if 'state' not in request.data:
            return Response({'error': 'El campo state es requerido'}, status=400)
        order.state = request.data['state']
        order.save()
        return Response({'message': 'Estado de la orden actualizado exitosamente'})

    def delete(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        order.products.clear()
        order.delete()
        return Response({'message': 'Orden eliminada exitosamente'})
