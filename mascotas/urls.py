from django.urls import path
from . import views
from .Carrito import *


urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    
    path("provedores", views.provedores, name="provedores"),
    path("productos", views.productos, name="productos"),
    
    path("usuarios", views.usuarios, name="usuarios"),
    path("reservas", views.reservas, name="reservas"),
    path("adminreservas", views.adminreservas, name="adminreservas"),
    path("dashboardhome", views.dashboard, name="dashboard"),
    
    path("payment_success/<int:id>", views.payment_success, name="payment_success"),
    # API Routes
    path("profile/<int:id>", views.editUser, name="edituser"),
    path("productos/<int:id>", views.editProducto, name="productdetail"),
    path("productosList", views.productosList, name="productosList"),
    path("reserva/<int:id>", views.reservaUser, name="reservaUser"),
    path("categorias/", views.allCat, name="allcat"),
    path("categoria/delete/<int:id>", views.deleteCat, name="deletecat"),
    path("usuarios/delete/<int:id>", views.deleteUser, name="deleteuser"),
    path("productos/delete/<int:id>", views.deleteProducto, name="deleteproducto"),
    path("provedores/delete/<int:id>", views.deleteProvedor, name="deleteprovedor"),
    path("mascota/delete/<int:id>", views.deleteMascota, name="deletemascota"),
    #Payments STRIPE Routes
    path("create-checkout-session/<int:id>", views.create_checkout_session, name="create_checkout_session"),
    path("failed/<int:id>", views.payment_failed, name="failed"),
  
   
    # Payments PayPal Routes
    path("pago-paypal/<int:id>", views.create_payment, name="pago-paypal"),
    path('execute_payment/', views.execute_payment, name='execute_payment'),
    path('payment_failed', views.payment_failed, name='payment_failed'),

    #Carrito Routes

    path('agregar/<int:producto_id>/', views.agregar_producto, name="agregar_producto"),
    path('eliminar/<int:producto_id>/', views.eliminar_producto, name="eliminar_producto"),
    path('restar/<int:producto_id>/', views.restar_producto, name="restar_producto"),
    path('limpiar/', views.limpiar_carrito, name="clean_carrito"),
    path('total_carrito/', views.total_carrito, name="total_carrito"),
]