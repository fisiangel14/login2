from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def fisrtLogin(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        nombre = request.POST.get('username')
        passWord = request.POST.get('password')

        userAuth = authenticate(request, username=nombre, password=passWord)
        print("------------")
        print(userAuth)
        print("------------")

        if userAuth:
            login(request, userAuth)
            return redirect('home')

        return render(request, 'login/login.html',{'error':"siga intentanto xddd nosea hacker"})
    
    print(request.user.is_authenticated)
    return render(request, 'login/login.html')

def home(request):
    return render(request, 'login/home.html')