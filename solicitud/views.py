from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def solicitud_producto(request):
    return render(request, 'solicitud/solicitud_producto.html')