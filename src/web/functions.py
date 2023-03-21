
from app.models import *
from .models import *

def get_user(data=dict()):
    return User.objects.all()