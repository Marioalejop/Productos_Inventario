from django.urls import path
from . import views

app_name = "pedidos"

urlpatterns = [
    path('', views.pedido_list, name='pedido_list'),
    path('crear/', views.pedido_create, name='pedido_create'),
    path('<int:pedido_id>/', views.pedido_detail, name='pedido_detail'),
]
