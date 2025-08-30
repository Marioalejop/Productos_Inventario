from django.shortcuts import render, redirect
import requests

API_URL = "https://localhost:7024/api/Clientes"

def clientes_lista(request):
    response = requests.get(API_URL, verify=False)
    clientes = response.json() if response.status_code == 200 else []
    return render(request, 'clientes/lista.html', {'clientes': clientes})

def cliente_crear(request):
    if request.method == 'POST':
        data = {
            "nombre": request.POST['nombre'],
            "apellido": request.POST['apellido'],
            "telefono": request.POST['telefono'],
            "correo": request.POST['correo']
        }
        requests.post(API_URL, json=data, verify=False)
        return redirect('clientes_lista')
    return render(request, 'clientes/crear.html')

def cliente_editar(request, id):
    if request.method == 'POST':
        data = {
            "id": id,
            "nombre": request.POST['nombre'],
            "apellido": request.POST['apellido'],
            "telefono": request.POST['telefono'],
            "correo": request.POST['correo']
        }
        requests.put(f"{API_URL}/{id}", json=data, verify=False)
        return redirect('clientes_lista')
    cliente = requests.get(f"{API_URL}/{id}", verify=False).json()
    return render(request, 'clientes/editar.html', {'cliente': cliente})

def cliente_eliminar(request, id):
    requests.delete(f"{API_URL}/{id}", verify=False)
    return redirect('clientes_lista')
