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
    path("mascota/delete/<int:id>", views.deleteMascota, name="deletemascota"),

    #Payments STRIPE Routes
    path("create-checkout-session/<int:id>", views.create_checkout_session, name="create_checkout_session"),
    # path("create-checkout-session-carrito", views.create_checkout_session_carrito, name="create_checkout_session_carrito"),
    path("failed/<int:id>", views.payment_failed, name="failed"),
    path("payment_success/<int:id>", views.payment_success, name="payment_success"),
    
    # Payments PayPal Routes
    path("pago-paypal/<int:id>", views.create_payment, name="pago-paypal"),
    path("pago-paypal/carrito/", views.create_payment_carrito, name="pago-paypal-carrito"),
    path('execute_payment/', views.execute_payment, name='execute_payment'),
    path('payment_failed', views.payment_failed, name='payment_failed'),

    #Carrito Routes

    path('agregar/<int:producto_id>/', views.agregar_producto, name="agregar_producto"),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name="eliminar_producto"),
    path('restar/<int:producto_id>/', views.restar_producto, name="restar_producto"),
    path('limpiar/', views.limpiar_carrito, name="clean_carrito"),
    path('total_carrito/', views.total_carrito, name="total_carrito"),
]