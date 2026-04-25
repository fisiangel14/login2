from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        nombre = request.POST.get('username')
        passWord = request.POST.get('password')
        next_url = request.POST.get('next', '')

        userAuth = authenticate(request, username=nombre, password=passWord)
        
        if userAuth:
            login(request, userAuth)
            return redirect(next_url or 'home')
        
        return render(request, 'login/login.html',{
            'error':"Usuario o contraseña incorrectos", 
            'next': next_url
        })
    
    next_url = request.GET.get('next', '')
    return render(request, 'login/login.html', {'next': next_url})

@login_required
def home(request):
    return render(request, 'login/home.html')

def logout_view(request):
    logout(request)
    return redirect('login')