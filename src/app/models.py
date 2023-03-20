from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Convention(models.Model):
    date_add = models.DateTimeField( auto_now=False, auto_now_add=True)
    date_update = models.DateTimeField( auto_now=True, auto_now_add=False)
    publish = models.BooleanField(default=False)

    class Meta:
        abstract = True


class User(AbstractUser):
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=50, blank=True, null=True)
    type_acteur = models.CharField(max_length=250, blank=True, null=True)
    acteur = models.CharField(max_length=250, blank=True, null=True)
    description = models.TextField()
    
    

class TypeActeur(Convention):
    code_type_acteur = models.CharField(max_length=150)
    nom_type_acteur = models.CharField(max_length=250, default="agriculteur")
    libele = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nom_type_acteur


class Acteur(Convention):
    code_acteur = models.CharField(max_length=50)
    nom = models.CharField(max_length=250,  null=True, blank=True)
    coordonnee = models.CharField(max_length=250,  null=True, blank=True)
    categorie = models.CharField(max_length=250,  null=True, blank=True)
    picture = models.FileField(upload_to="acteur_img")
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField() 
    def __str__(self):
        return self.nom