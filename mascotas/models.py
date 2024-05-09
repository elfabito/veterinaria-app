from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django import forms
from django.dispatch import receiver
from django.db.models.signals import post_save
from decimal import Decimal
# Create your models here.


class UserManager(BaseUserManager):
    
    use_in_migrations = True

    def _create_user(self, dni, email, password, **extra_fields):
        if not dni:
            raise ValueError('Users require an dni field')
        email = self.normalize_email(email)
        
        user = self.model(dni=dni, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, dni, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_veterinario', False)
        extra_fields.setdefault('is_provedor', False)
        return self._create_user(dni=dni, email=email, password=password,first_name=first_name.title(), last_name=last_name.title(), **extra_fields)

    def create_superuser(self, dni, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_provedor', True)
        extra_fields.setdefault('is_veterinario', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(dni=dni, email=email, password=password,first_name=first_name.title(), last_name=last_name.title(), **extra_fields)
   


    def serialize(self):
        return {
            "id": self.id,
            "dni": self.dni,
            "email": self.email,
            "is_doctor" : self.is_veterinario,
            "is_provedor": self.is_provedor,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,            
        }
    

class CustomUser(AbstractUser):
    
    username = None
    is_veterinario = models.BooleanField(default=False)
    is_provedor = models.BooleanField(default=False)
    email = models.EmailField(db_index=True, unique=True, max_length=250)
    dni = models.CharField(unique=True, max_length=8, null=True, blank=True)
    objects = UserManager()
    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} "

    def serialize(self):
        return {

            "id": self.id,
            "dni":self.dni,
            "email": self.email,
            "is_veterinario" : self.is_veterinario,
            "is_provedor": self.is_provedor,
            "first_name": self.first_name,
            "last_name": self.last_name,
                        
        }
    
    
class Mascota(models.Model):
    
    idMascota = models.AutoField(primary_key=True)
    propietario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="mascota")
    nombre = models.CharField(max_length=17, blank=True)
    image = models.ImageField(blank=True, null=True, upload_to="images/")
    especie = models.CharField(max_length=17, blank=True)
    raza = models.CharField(max_length=100, blank=True)
    edad = models.IntegerField()
    fechaNac = models.DateField()

    def __str__(self):
        return f"{self.propietario} | {self.nombre} (raza): {self.raza}"

    def serialize(self):
        return {

            "propietario": self.propietario,
            "nombre":self.nombre,
            "especie": self.especie,
            "raza" : self.raza,
            "edad": self.edad,
            "fechaNac": self.fechaNac,              
            
        }
    
class HistoriaMedica(models.Model):

    idHistoria = models.AutoField(primary_key=True)
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    fechaConsulta = models.DateTimeField(auto_now_add=True)
    diagnostico = models.TextField(max_length=255)
    tratamiento = models.TextField(max_length=255)

    def __str__(self):
        return f"{self.mascota.propietario.first_name} | {self.mascota} {self.fechaConsulta} (raza): {self.raza}"

    def serialize(self):
        return {

            "mascota": self.mascota,
            "fechaConsulta":self.fechaConsulta,
            "diagnostico": self.diagnostico,
            "tratamiento" : self.tratamiento,
           
        }
    
class Provedor(models.Model):
     
     idProvedor = models.AutoField(primary_key=True)
     provedor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="provedor")
     razonSocial = models.TextField(max_length=30)
     rut  = models.TextField(blank=True, null=True)
     domicilio = models.TextField(max_length=255, blank=True, null=True)
     telefono = models.TextField(max_length=25, blank=True, null=True)
     
     def __str__(self):
        return self.provedor.first_name
     
     def serialize(self):
        return {
            "idProvedor": self.idProvedor,
            "provedor": self.provedor,
            "first_name": self.provedor.first_name,
            "last_name": self.provedor.last_name,
            "email" : self.provedor.email,
            "razonSocial":self.razonSocial,
            "rut": self.rut,
            "domicilio" : self.domicilio,
            "telefono" : self.telefono,
           
        }

@receiver(post_save, sender=CustomUser)
def vendedor(sender, instance, created, **kwargs):

    if created and instance.is_provedor:
        vendedor =Provedor(provedor=instance)
        vendedor.save()
    

class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    def serialize(self):
        return  self.name,
    
class Producto(models.Model):
    idProducto = models.AutoField(primary_key=True)
    vendedor = models.ForeignKey(Provedor, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to="images/")
    precio = models.IntegerField()
    cantidad = models.IntegerField(default=1)
    categoria = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.nombre
    

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields=['nombre','descripcion','image', 'categoria', 'cantidad', 'precio']
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'description':forms.Textarea(attrs={'class':'form-control'}),
            'image':forms.TextInput(attrs={'class':'form-control'}),          
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields=['name']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),         
        }

class Service(models.Model):
    name = models.CharField(max_length=50)
    precio = models.IntegerField()

    def __str__(self):
        return self.name
    
    def serialize(self):
        return {
            "name": self.name,
            "precio": self.precio,          
        }
    
class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields=['name','precio']
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),     
        }
        
class Appointment(models.Model):

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    datetime_ordered = models.DateTimeField(blank=False, null=False)
    comment = models.TextField( blank=True)
    time_ordered = models.DateTimeField(null=False, blank=False,auto_now_add=True)
    canceled = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.first_name} | day: {self.datetime_ordered} | service: {self.service} | timeorder: {self.time_ordered}"
    
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.first_name,
            "email": self.user.email,
            "service": self.service,
            "datetime" : self.datetime,
            "comment": self.comment,        
            "time_ordered": self.time_ordered,
            "approved": self.approved,
            "canceled": self.canceled,
        }
    
