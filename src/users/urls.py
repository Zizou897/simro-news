from django.urls import path
from django.contrib.auth import views as auth_views

from  .api_views import sign_out, SignUpView, LoginView


urlpatterns = [
    # Api link
    path('api/register/', SignUpView.as_view(), name='signup'),
    path('api/login/', LoginView.as_view(), name='signin'),
    path('api/logout/', sign_out, name='signout'),

]
