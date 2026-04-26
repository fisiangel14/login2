from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        #Validar campos vacíos
        if not username or not password or not password_confirm:
            return render(request, 'login/register.html', {'error': 'Todos los campos son obligatorios'})
        #Validar confirmación de password
        if password != password_confirm:
            return render(request, 'login/register.html', {'error': 'Las contraseñas no coinciden'})
        #Validar si el usuario existe
        if User.objects.filter(username=username).exists():
            return render(request, 'login/register.html', {'error': 'El nombre de usuario ya existe'})

        User.objects.create_user(username=username, password=password)
        return redirect('login')
    
    return render(request,'login/register.html')

#API
@csrf_exempt
def api_login_view(request):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'Método no permitido'}, status=405)
    
    data = json.loads(request.body)

    username = data.get('username', '').strip()
    password = data.get('password')

    if not username or not password:
        return JsonResponse({'ok':False, 'error':'Campos obligatorios'}, status=400)
    
    user = authenticate(request, username=username, password=password)

    if user:
        return JsonResponse({
            'ok': True,
            'message': 'Login correcto'
        })
    
    return JsonResponse({'ok':False,'error':'Credenciales incorrectas'}, status=401)

@csrf_exempt
def api_register_view(request):
    if request.method != 'POST':
        return JsonResponse({'ok': False, 'error': 'Método no permitido'}, status=405)
    
    try:
        data = json.loads(request.body)
    except:
        return JsonResponse({'ok': False, 'error': 'JSON inválido'}, status=400)

    username = data.get('username', '').strip()
    password = data.get('password')
    password_confirm = data.get('password_confirm')

    if not username or not password or not password_confirm:
        return JsonResponse({'ok':False, 'error':'Campos obligatorios'}, status=400)
    
    if password != password_confirm:
        return JsonResponse({'ok':False,'error':'Las contraseñas no coinciden'}, status=400)
    
    if  User.objects.filter(username=username).exists():
        return JsonResponse({'ok':False, 'error':'El usuario ya existe'},status=400)
    
    User.objects.create_user(username=username, password=password)

    return JsonResponse({
        'ok': True,
        'message': 'Usuario creado correctamente'
    },status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_me(request):
    return Response({
        'username': request.user.username
    })

