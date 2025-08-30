from django.urls import path
from . import views

app_name = "movimientos"

urlpatterns = [
    path('', views.movimiento_list, name='movimiento_list'),
    path('entrada/', views.movimiento_entrada, name='movimiento_entrada'),
    path('salida/', views.movimiento_salida, name='movimiento_salida'),
]
