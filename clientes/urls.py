from django.urls import path
from . import views

urlpatterns = [
    path('', views.clientes_lista, name='clientes_lista'),
    path('crear/', views.cliente_crear, name='cliente_crear'),
    path('editar/<int:id>/', views.cliente_editar, name='cliente_editar'),
    path('eliminar/<int:id>/', views.cliente_eliminar, name='cliente_eliminar'),
]