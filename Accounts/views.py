
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import status
from rest_framework.authtoken.models import Token
  
from django.contrib.auth.models import User
from Accounts.serializer import UserSerializer
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist

@api_view(['POST'])
def registerView(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.filter(username=serializer.data['username'])
        return Response(serializer.data)
    else:
        return Response(serializer.error_messages)

@api_view(['POST'])
def loginView(request):
    try:
        user = User.objects.get(username=request.data['username'])
        if check_password(request.data['password'], user.password): 
            authenticate(request=request, username=request.data['username'], password=request.data['password'])
            login(request, user)
            token = Token.objects.filter(user=user)
            if not token:
                token = Token.objects.create(user=user)
            else:
                token = token[0]
                     
            return Response(
                {
                    'token' : token.key,
                    "username" : user.username
                }
            )
        else:
            return Response({"message" : "Incorrect password"}, status=status.HTTP_403_FORBIDDEN)
    except ObjectDoesNotExist:
        return Response({"message" : "UserAccount doesn't exist"}, status=status.HTTP_403_FORBIDDEN)
        
@api_view(['POST'])
def logoutView(request):
    try:
        token = Token.objects.filter(key=request.data["token"])
        # print(token)
        logout(request)
        return Response({
            "message" : "Logout Succesfully"
            },
            status=status.HTTP_200_OK
        )
    except:
        return Response({
            "message" : "You haven't Signed up"
        },
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
def getUser(request):
    try:
        user = User.objects.get(username=request.GET['username'])
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except:
        return Response({"message" : "Account Does't exist"}, status=status.HTTP_403_FORBIDDEN)
