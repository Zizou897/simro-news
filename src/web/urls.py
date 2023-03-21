from django.urls import path
from .views import *

urlpatterns = [
     
    path('auth/login/', logIn, name="login"),
    path('auth/login/', logOut, name="logout"),
    path('dashboard/', home, name="dashboard"),
    path('user/', user_list, name="userList")

]
