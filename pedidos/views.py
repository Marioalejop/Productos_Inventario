import requests
from django.shortcuts import render, redirect
from django.conf import settings

API_URL = "https://localhost:7024/api/Pedidos"

def pedido_list(request):
    response = requests.get(API_URL, verify=False)
    pedidos = response.json() if response.status_code == 200 else []
    return render(request, "pedidos/lista.html", {"pedidos": pedidos})

def pedido_create(request):
    if request.method == "POST":
        data = {
            "clienteId": request.POST.get("clienteId"),
            "productos": request.POST.getlist("productos"),  # luego lo hacemos dinámico
        }
        requests.post(API_URL, json=data, verify=False)
        return redirect("pedidos:pedido_list")
    return render(request, "pedidos/crear.html")

def pedido_detail(request, pedido_id):
    response = requests.get(f"{API_URL}/{pedido_id}", verify=False)
    pedido = response.json() if response.status_code == 200 else None
    return render(request, "pedidos/detalle.html", {"pedido": pedido})
