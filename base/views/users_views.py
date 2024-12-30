from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from base.serializers import UserSerializer, UserSerializerWithToken
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from base.models import Tasks
from django.contrib.auth import authenticate

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
   def validate(self, attrs):
       data = super().validate(attrs)
       serializer = UserSerializerWithToken(self.user).data
       for key, value in serializer.items():
           data[key] = value

       return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    
    

@api_view(['POST'])
def loginUser(request):
    data = request.data
    user = authenticate(username=data['email'], password=data['password'])
    if user:
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    else:
        message = 'Invalid credentials'
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserDetails(request, pk):
     
     user = request.user
     user_pk = user.pk
     user_object = User.objects.get(pk=user_pk)
     serializer = UserSerializer(user_object, many=False)
     return Response(serializer.data)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfileDetails(request, pk):
    user = User.objects.get(pk=pk)
    data = request.data

    user.first_name = data.get('first_name', user.first_name)
    user.username = data.get('email', user.username)
    user.email = data.get('email', user.email)
    password = data.get('password', None)
    if password and password != '':
        user.password = make_password(data['password'])
    user.save()
    serializer = UserSerializerWithToken(user, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteUser(request, pk):
    user = User.objects.get(pk=pk)
    user.delete()
    return Response("User deleted successfully", status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def registerUser(request):
    try:
        data = request.data
        user = User.objects.create(
            first_name = data['first_name'],
            username = data['email'],
            email = data['email'],
            password = make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = 'User with this email already exists'
        return Response(message, status=status.HTTP_400_BAD_REQUEST)