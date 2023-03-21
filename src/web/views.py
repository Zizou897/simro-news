from django.shortcuts import redirect, render

from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required

from .functions import *

# Create your views here.
def logIn(request):
    
    if  request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("######1######")
        print(password)
        my_user = authenticate(request,username=username, password=password)
        if  my_user is not None:
            print("######4######")
            login(request, my_user)
            print(username)
            return redirect("dashboard")
    template_name = 'auth/login.html'
    context = {
        
    }
    return render(request, template_name, context)


@login_required(login_url="login")
def logOut(request):
    logout(request)
    return redirect("login")



@login_required(login_url="login")
def home(request):
    
    template_name = 'pages/layout/index.html'
    context = {
        
    }
    return render(request, template_name, context)


@login_required(login_url="login")
def user_list(request):
    
    if request.method == 'POST':
        contact = request.POST.get('phone')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        fonction = request.POST.get('fonction')
        access = request.POST.get('access')
        description = request.POST.get('description')
        
        """ 
        from django.contrib import messages

         from django.core.exceptions import ValidationError
        
        if not username or username.isspace() or not email or email.isspace() or not phone or phone.isspace() or not address or address.isspace() or not password or password.isspace():
            messages.error(request, 'Veuillez remplir tous champs !!!')
            return redirect("register")
        
        if User.objects.filter(username=username):
            messages.error(request, 'username existant')
            return redirect("register")
        if verify_email(email):
            messages.error(request,'email incorrect')
            return redirect('register')
        print("######1######")
        
        if password != password1:
            messages.error(request,'les deux mots de passes doivent etre identique')
            print("######2######")
            return redirect('register')
        else:
            print("######3######")
            user = User.objects.create_user(username=username, email=email, phone=phone, address=address, password=password)
            user.is_active = False
            user.save()
            print(password)
            return redirect("login")
        
        """
        print(password)
    
    get_users =  get_user()
    template_name = 'pages/layout/userList.html'
    context = {
        'get_users': get_users,
    }
    return render(request, template_name, context)

