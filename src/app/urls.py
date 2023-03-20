from django.urls import path
from django.contrib.auth import views as auth_views

from  .api_views import *
from .views import doc

urlpatterns = [
    
    # documentation Api
    path('api/documentation/', doc),
    
    # authenticate Api link
    path('api/register/', SignUpView.as_view(), name='signup'),
    path('api/login/', LoginView.as_view(), name='signin'),
    path('api/logout/', sign_out, name='signout'),
    
    #Api for User
    path('api/user/', UserList.as_view()),
    path('api/user/<int:pk>/detail', UserList.as_view()),
    path('api/user/<int:pk>/update', UserList.as_view()),
    path('api/user/<int:pk>/delete', UserList.as_view()),
    
    
    # Api for action
    path('api/type-acteur/', TypeActeurCreateApiView.as_view()),
    path('api/type-acteur/<int:pk>/detail', TypeActeurCreateApiView.as_view()),

]
