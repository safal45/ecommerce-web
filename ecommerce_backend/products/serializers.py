
from rest_framework import serializers
from .models import Product,User,Order

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'image','created','updated']

from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'address']

    def create(self, validated_data):
        # Hash the password before storing it
        validated_data['password'] = make_password(validated_data['password'])
        
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],  
            address=validated_data['address'],
        )
        return user

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'product', 'quantity', 'shipping_address', 'phone_number', 'created_at']

    def validate(self, data):
        product = data['product']
        quantity = data['quantity']

        # Check if there is enough stock
        if product.stock < quantity:
            raise serializers.ValidationError(f"Not enough stock for {product.name}. Only {product.stock} available.")
        
        return data

    def create(self, validated_data):
        product = validated_data['product']
        quantity = validated_data['quantity']

        # Subtract the quantity from the stock
        product.stock -= quantity
        product.save()

        # Create the order
        order = Order.objects.create(**validated_data)
        return order