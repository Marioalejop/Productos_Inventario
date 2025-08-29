from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth.models import User

@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')

def login_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            error = "Usuario o contraseña incorrectos"
    return render(request, "login.html", {"error": error})

def logout_view(request):
    logout(request)
    return redirect('login')

def signup_view(request):
    error = None
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")
        email = request.POST.get("email")
        if password != password2:
            error = "Las contraseñas no coinciden"
        elif User.objects.filter(username=username).exists():
            error = "El usuario ya existe"
        else:
            User.objects.create_user(username=username, password=password, email=email)
            return redirect('login')
    return render(request, "signup.html", {"error": error})
