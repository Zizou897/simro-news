from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.validators import validate_email
from django.contrib.auth import authenticate

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.request import Request

from drf_yasg.utils import swagger_auto_schema

from .serializer import UserSerializer


User = get_user_model()

class SignUpView(generics.GenericAPIView):
    serializer_class = UserSerializer
    
   
    def post(self, request:Request):
        data = request.data
        serializer = self.serializer_class(data=data)
        
        if serializer.is_valid():
            serializer.save()
            
            response = {
                "code": 1,
                "status": status.HTTP_200_OK,
                "message": "L'utlisateur est bel et bien enregistré",
                "data": serializer.data
            }
            
            return Response(data=response, status=status.HTTP_200_OK)
        
        response = {
            "code": 0,
            "status": status.HTTP_200_OK,
            "message": "L'utlisateur non enregistré",
            "data": serializer.errors
        }
        
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):

    def post(self, request:Request):
        username = request.data.get('username')
        password = request.data.get('password')
        #my_user = User.objects.get(username=username)
       
        user = authenticate(username=username, password=password)
        print(user)
        
        if user is not None:
            if user.is_active:
                try:
                   token = Token.objects.get(user_id=user.id)
                except Token.DoesNotExist:
                    token = Token.objects.create(user=user)
                    token.save()
                    
                response = {
                    "code": 1,
                    "status": status.HTTP_200_OK,
                    "message": "vous etes connecté",
                    "token":  user.auth_token.key,
                    "user":{
                        "username": user.username,
                        "email": user.email,
                        "phone": user.phone,
                    }
                }
                
                return Response(data=response, status=status.HTTP_201_CREATED)
            else:
                
                response = {
                    "code": 0,
                    "status": status.HTTP_201_CREATED,
                    "message": "votre compte n'est pas actif, veuillez contacter l'admin",
                    "token":  None,
                    "user": None
                }
                return Response(data=response, status=status.HTTP_201_CREATED)
                
        response = {
            "code": 0,
            "status": status.HTTP_201_CREATED,
            "message": "username ou mot de passe incorrect",
            "user": None
        }
        return Response(data=response, status=status.HTTP_201_CREATED)

        
        
    
    
    def get(self, request:Request):
        content = {
            "user": str(request.user),
            "auth": str(request.auth)
        }
        
        return Response(data=content, status=status.HTTP_200_OK)


#----------------------------------------------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sign_out(request):
    
    Token.objects.filter(user=request.user).delete()
    logout(request)
    
    response = {
        "code": 1,
        "status": status.HTTP_200_OK,
        "message": "utilisateur déconnecté",
       
    }
    return Response(data=response, status=status.HTTP_200_OK)

#-----------------------------------------------------------
