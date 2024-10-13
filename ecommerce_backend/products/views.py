from rest_framework import viewsets
from .models import Product,User,Order
from .serializers import ProductSerializer,UserSerializer,OrderSerializer
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth.hashers import make_password,check_password

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class = UserSerializer

@api_view(['POST'])
def login_view(request):
    try:
        email = request.data.get('email', '').lower()  # Convert email to lowercase
        password = request.data.get('password')


        # Direct query to find user by email
        user = User.objects.filter(email=email).first()

        if user is not None:
            print(f"User found: {user}")
            
            # If passwords match, return success
            if check_password(password, user.password):  # Change to use password hashing later
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                print("Password mismatch")  # Password didn't match
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            print("User not found")  # No user found with the email
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print(f"Error: {e}")
        return Response({'message': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def signup_view(request):
    # Extract data from the request
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    address = request.data.get('address')

    # Check if all required fields are provided
    if not username or not email or not password or not address:
        return JsonResponse({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the email already exists
    if User.objects.filter(email=email).exists():
        return JsonResponse({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new user
    hashed_password = make_password(password)
    user = User(username=username, email=email, password=hashed_password, address=address)
    user.save()

    # Return a success response
    return JsonResponse({'message': 'User created successfully!'}, status=status.HTTP_201_CREATED)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


@api_view(['POST'])
def order_view(request):
    serializer = OrderSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
