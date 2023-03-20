from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.db.models import Q



class Email_OR_Phone(BaseBackend):
    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
    
    def authenticate(self, request, username=None, password=None):
        Users = get_user_model()
        
        try:
            user = Users.objects.get(Q(phone__iexact=username) | Q(email__iexact=username))
            if user.check_password(password):
                return user
        except Users.DoesNotExist:
            return None