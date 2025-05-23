from rest_framework import serializers
from .models import User, Product, Order, OrderProduct
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderProductSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = OrderProduct
        fields = ['product', 'product_id', 'quantity']
        read_only_fields = ['product']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['product'] = ProductSerializer(instance.product).data
        return representation

class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(source='orderproduct_set', many=True)

    class Meta:
        model = Order
        fields = ['id', 'name', 'address', 'phone', 'products']

    def create(self, validated_data):
        products_data = validated_data.pop('orderproduct_set')
        order = Order.objects.create(**validated_data)
        for product_data in products_data:
            OrderProduct.objects.create(order=order, product_id=product_data['product_id'], quantity=product_data['quantity'])
        return order

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        order_products = OrderProduct.objects.filter(order=instance)
        representation['products'] = OrderProductSerializer(order_products, many=True).data
        return representation