from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.validators import validate_email
from django.contrib.auth import authenticate

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
    
    @swagger_auto_schema(
        operation_summary="L'api pour l'enregistrement d'un utilisateur ",
        operation_description=" Cette Api crée un user avec differents champs"
    )
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
            
            return Response(data=response, status=status.HTTP_201_CREATED)
        
        response = {
            "code": 0,
            "status": status.HTTP_200_OK,
            "message": "L'utlisateur non enregistré",
            "data": serializer.errors
        }
        
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @swagger_auto_schema(
        operation_summary="L'api de connexion",
        operation_description=" Cette Api permet au user de s'authentifier avec le username et le mot de passe"
    )
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
                
                return Response(data=response, status=status.HTTP_200_OK)
            else:
                
                response = {
                    "code": 0,
                    "status": status.HTTP_200_OK,
                    "message": "votre compte n'est pas actif, veuillez contacter l'admin",
                    "token":  None,
                    "user": None
                }
                return Response(data=response)
                
        response = {
            "code": 0,
            "status": status.HTTP_200_OK,
            "message": "username ou mot de passe incorrect",
            "user": None
        }
        return Response(data=response)

        
        
    
    @swagger_auto_schema(
        operation_summary="L'api de connexion(verification)",
        operation_description=" Cette Api permet de verifier si le user est autifier \ndans le cas contraire il renvoie Anonymos\n{\n \t \"user\": \"Anonymos,\"\n \t\"auth\":None\n}"
    )
    def get(self, request:Request):
        content = {
            "user": str(request.user),
            "auth": str(request.auth)
        }
        
        return Response(data=content, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sign_out(request):
    
    message = ''


    Token.objects.filter(user=request.user).delete()
    logout(request)
    
    message = 'utilisateur déconnecté'

    return Response(data={'mesdage':message}, status=status.HTTP_200_OK)
