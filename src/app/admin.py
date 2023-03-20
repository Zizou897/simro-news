from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone','is_active')


@admin.register(TypeActeur)
class TypeActeurAdmin(admin.ModelAdmin):
   list_display = ('code_type_acteur', 'nom_type_acteur', 'libele', 'publish')
    