import requests
from django.shortcuts import render, redirect
from django.conf import settings

API_URL = "https://localhost:7024/api/Movimientos"

def movimiento_list(request):
    response = requests.get(API_URL, verify=False)
    movimientos = response.json() if response.status_code == 200 else []
    return render(request, "movimientos/lista.html", {"movimientos": movimientos})

def movimiento_entrada(request):
    if request.method == "POST":
        data = {
            "productoId": request.POST.get("productoId"),
            "cantidad": request.POST.get("cantidad"),
            "tipo": "entrada",
        }
        requests.post(API_URL, json=data, verify=False)
        return redirect("movimientos:movimiento_list")
    return render(request, "movimientos/entrada.html")

def movimiento_salida(request):
    if request.method == "POST":
        data = {
            "productoId": request.POST.get("productoId"),
            "cantidad": request.POST.get("cantidad"),
            "tipo": "salida",
        }
        requests.post(API_URL, json=data, verify=False)
        return redirect("movimientos:movimiento_list")
    return render(request, "movimientos/salida.html")
