from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token
from decouple import config
import httpx

API_BASE = config('API_BASE_URL')
TIMEOUT = 10.0

def _auth_headers(request):
    headers = {"Accept": "application/json"}
    token = request.session.get('jwt')
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

def home(request):
    return render(request, "home.html")

@require_http_methods(["GET"])
def product_list(request):
    try:
        with httpx.Client(timeout=TIMEOUT, verify=False) as client:
            r = client.get(f"{API_BASE}/api/productos", headers=_auth_headers(request))
            r.raise_for_status()
            productos = r.json()
    except httpx.HTTPError as e:
        messages.error(request, f"Error al cargar productos: {e}")
        productos = []
    return render(request, "productos/list.html", {"productos": productos})

@require_http_methods(["GET"])
def product_detail(request, id: int):
    try:
        with httpx.Client(timeout=TIMEOUT, verify=False) as client:
            r = client.get(f"{API_BASE}/api/productos/{id}", headers=_auth_headers(request))
            r.raise_for_status()
            producto = r.json()
    except httpx.HTTPError as e:
        messages.error(request, f"No se pudo cargar el producto: {e}")
        return redirect("product_list")
    return render(request, "productos/detail.html", {"producto": producto})

@require_http_methods(["GET", "POST"])
def product_create(request):
    if request.method == "GET":
        get_token(request)
        return render(request, "productos/create.html")

    payload = {
        "nombre": request.POST.get("nombre"),
        "precio": float(request.POST.get("precio") or 0),
        "stock": int(request.POST.get("stock") or 0),
    }
    try:
        with httpx.Client(timeout=TIMEOUT, verify=False) as client:
            r = client.post(f"{API_BASE}/api/productos", json=payload, headers=_auth_headers(request))
            r.raise_for_status()
            messages.success(request, "Producto creado correctamente.")
            return redirect("product_list")
    except httpx.HTTPError as e:
        messages.error(request, f"Error al crear producto: {e}")
        return render(request, "productos/create.html", {"formdata": payload})

@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.method == "GET":
        get_token(request)
        return render(request, "auth/login.html")

    payload = {
        "username": request.POST.get("username"),
        "password": request.POST.get("password"),
    }
    try:
        with httpx.Client(timeout=TIMEOUT, verify=False) as client:
            r = client.post(f"{API_BASE}/api/auth/login", json=payload)
            r.raise_for_status()
            data = r.json()
            token = data.get("token") or data.get("access_token")
            if not token:
                messages.error(request, "No se recibió token JWT.")
                return redirect("login")
            request.session['jwt'] = token
            messages.success(request, "Sesión iniciada.")
            return redirect("home")
    except httpx.HTTPError as e:
        messages.error(request, f"Login inválido: {e}")
        return redirect("login")

def logout_view(request):
    request.session.pop('jwt', None)
    messages.info(request, "Sesión cerrada.")
    return redirect("home")