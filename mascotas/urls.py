from django.urls import path
from . import views
from .Carrito import *

from django.contrib.auth.views import (
    
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    
    #PDF 
    path('lista-usuarios', views.ListUsuariosPdf.as_view(), name='all_usuarios'),
    path('lista-productos', views.ListProductsPdf.as_view(), name='all_products'),
    path('lista-reservas', views.ListReservasPdf.as_view(), name='all_reservas'),
    path('lista-provedores', views.ListProvedoresPdf.as_view(), name='all_provedores'),

    #PASSWORD RESET
    path('password-reset/', PasswordResetView.as_view(template_name='users/password_reset_form.html'),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),
    
    path("adminPanel/provedores", views.provedores, name="provedores"),
    path("adminPanel/productos", views.productos, name="productos"),
    path("adminPanel/usuarios", views.usuarios, name="usuarios"),
    path("adminPanel/reservas", views.adminreservas, name="adminreservas"),
    path("adminPanel/", views.dashboard, name="dashboard"),

    path("reservas", views.reservas, name="reservas"),
    
    # API Routes
    path("profile/<int:id>", views.editUser, name="edituser"),
    path("productos/<int:id>", views.editProducto, name="productdetail"),
    path("productosList", views.productosList, name="productosList"),
    path("adminPanel/reserva/<int:id>", views.reservaUser, name="reservaUser"),
    path("categorias/", views.allCat, name="allcat"),
    path("categoria/delete/<int:id>", views.deleteCat, name="deletecat"),
    path("usuarios/delete/<int:id>", views.deleteUser, name="deleteuser"),
    path("productos/delete/<int:id>", views.deleteProducto, name="deleteproducto"),
    path("provedores/delete/<int:id>", views.deleteProvedor, name="deleteprovedor"),
    path("service/delete/<int:id>", views.deleteServicio, name="deleteservice"),
    path("mascota/delete/<int:id>", views.deleteMascota, name="deletemascota"),


    #Carrito Routes

    path('agregar/<int:producto_id>/', views.agregar_producto, name="agregar_producto"),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name="eliminar_producto"),
    path('restar/<int:producto_id>/', views.restar_producto, name="restar_producto"),
    path('limpiar/', views.limpiar_carrito, name="clean_carrito"),
    path('total_carrito/', views.total_carrito, name="total_carrito"),
]