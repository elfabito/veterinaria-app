from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("provedores", views.provedores, name="provedores"),
    path("productos", views.productos, name="productos"),
    path("usuarios", views.usuarios, name="usuarios"),
    path("reservas", views.reservas, name="reservas"),
    path("adminreservas", views.adminreservas, name="adminreservas"),



    # API Routes
    path("profile/<int:id>", views.editUser, name="edituser"),
    path("productos/<int:id>", views.editProducto, name="editproducto"),
    path("reserva/<int:id>", views.reservaUser, name="reservaUser"),

    path("usuarios/delete/<int:id>", views.deleteUser, name="deleteuser"),
    path("productos/delete/<int:id>", views.deleteProducto, name="deleteproducto"),
    path("provedores/delete/<int:id>", views.deleteProvedor, name="deleteprovedor"),
    
    
]