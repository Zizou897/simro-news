from rest_framework import viewsets

from .models import *
from .serializer import *



class TypeACteurViewSet(viewsets.ModelViewSet):
    queryset = TypeActeur.objects.filter(publish=True)
    serializer_class = TypeActeurSerialiser 
    