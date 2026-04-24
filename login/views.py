from django.shortcuts import render, redirect

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect(request, 'home')
    
    return render(request, 'logint.html')