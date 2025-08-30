from django.shortcuts import render, redirect
import requests

API_URL = "https://localhost:7024/api/Productos"

def productos_lista(request):
    response = requests.get(API_URL, verify=False)  # quitar verify si hay problema con SSL
    productos = response.json() if response.status_code == 200 else []
    return render(request, 'productos/lista.html', {'productos': productos})

def producto_crear(request):
    if request.method == 'POST':
        data = {
            "nombre": request.POST['nombre'],
            "precio": request.POST['precio'],
            "stock": request.POST['stock']
        }
        requests.post(API_URL, json=data, verify=False)
        return redirect('productos_lista')
    return render(request, 'productos/crear.html')

def producto_editar(request, id):
    if request.method == 'POST':
        data = {
            "id": id,
            "nombre": request.POST['nombre'],
            "precio": request.POST['precio'],
            "stock": request.POST['stock']
        }
        requests.put(f"{API_URL}/{id}", json=data, verify=False)
        return redirect('productos_lista')
    producto = requests.get(f"{API_URL}/{id}", verify=False).json()
    return render(request, 'productos/editar.html', {'producto': producto})

def producto_eliminar(request, id):
    requests.delete(f"{API_URL}/{id}", verify=False)
    return redirect('productos_lista')
