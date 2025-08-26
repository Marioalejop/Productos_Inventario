from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('productos/', views.product_list, name='product_list'),
    path('productos/<int:id>/', views.product_detail, name='product_detail'),
    path('productos/nuevo/', views.product_create, name='product_create'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]