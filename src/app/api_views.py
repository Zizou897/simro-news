from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.validators import validate_email
from django.contrib.auth import authenticate

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, mixins, status
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from rest_framework.validators import ValidationError


from .models import *
from .serializer import *


User = get_user_model()

class SignUpView(generics.GenericAPIView):
    serializer_class = UserSerializer
    
   
    def post(self, request:Request):
        
        email_exists = User.objects.filter(email=request.data.get('email')).exists()
        phone_exists = User.objects.filter(phone=request.data.get('phone')).exists()
        data = request.data
        serializer = self.serializer_class(data=data)
        if email_exists:
            #raise ValidationError("email exists déjà")

            response = {
            "code": 0,
            "status": status.HTTP_201_CREATED,
            "message": "email exists déjà",
            "data": serializer.errors
            }
        
            return Response(data=response, status=status.HTTP_201_CREATED)
        
        
        if phone_exists:
            #raise ValidationError("numero de téléphone exists déjà")

            response = {
            "code": 0,
            "status": status.HTTP_201_CREATED,
            "message": "numero de téléphone exists déjà",
            #"data": serializer.errors
            }
        
            return Response(data=response, status=status.HTTP_201_CREATED)
        
        
        
        
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
            "status": status.HTTP_201_CREATED,
            "message": "L'utlisateur non enregistré",
            "data": serializer.errors
        }
        
        return Response(data=response, status=status.HTTP_201_CREATED)


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
                
                return Response(data=response, status=status.HTTP_200_OK)
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



class UserList(generics.GenericAPIView,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'
    
    
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)
    

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class TypeActeurCreateApiView(generics.GenericAPIView,
        mixins.ListModelMixin,
        mixins.RetrieveModelMixin,
        mixins.CreateModelMixin):
    queryset = TypeActeur.objects.filter(publish=True)
    serializer_class = TypeActeurSerialiser
    lookup_field = 'pk'
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response = {
            'code': 1,
            'status': status.HTTP_200_OK,
            'data': serializer.data
        }
        return Response(data=response, status=status.HTTP_200_OK, headers=headers)
    """
        response = {
            'code': 201
        }
        return Response(data=response, status=status.HTTP_201_CREATED, headers=headers)
    """
    
    def perform_create(self, serializer):
        code_type_acteur = serializer.validated_data.get('code_type_acteur')
        nom_type_acteur = serializer.validated_data.get('nom_type_acteur')
        libele = serializer.validated_data.get('libele')
        serializer.save()
    
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)