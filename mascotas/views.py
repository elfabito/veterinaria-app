from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib import messages
import json
from google_calendar_class import *
import datetime

#Create your views here.
from django.contrib.auth.decorators import login_required

def home(request):
    productos = Producto.objects.all()
    return render(request, "home.html", {"productos":productos})

@csrf_exempt
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        dni = request.POST["dni"]
        password = request.POST["password"]
        user = authenticate(request, dni=dni, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "login.html", {
                "message": "Invalid dni and/or password."
            })
    else:
        return render(request, "login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))


@csrf_exempt
def register(request):
    if request.method == "POST":
        
        first_name = request.POST["first_name"].capitalize()
        last_name = request.POST["last_name"].capitalize()
        dni = request.POST["dni"]
        email = request.POST["email"].lower()

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = CustomUser.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name, dni=dni)
           
            user.save()
            
        except IntegrityError:
            return render(request, "register.html", {
                "message": "We have a user register with that dni"
            })
        login(request, user)
        return HttpResponseRedirect(reverse("home"))
       
    else:
        return render(request, "register.html")
    
@csrf_exempt
def profile(request):
    propietario = CustomUser.objects.get(pk=request.user.id) 
    
    mascotas = Mascota.objects.filter(propietario=propietario)
    if request.method == "POST":
                
         
        nombre = request.POST["nombre"].capitalize()
        especie = request.POST["especie"].capitalize()
        raza = request.POST["raza"].capitalize()
        edad = request.POST["edad"]
        fechaNac = request.POST["fechaNac"]
        print(propietario)
        

        # Attempt to create new Mascota
        try:
            mascota = Mascota.objects.create(
                nombre=nombre,
                especie=especie, 
                raza=raza, 
                edad=edad, 
                fechaNac=fechaNac, 
                propietario = propietario
                )
           
            mascota.save()
            

        except IntegrityError:
            return render(request, "profile.html", {
                "message": "Hubo un problema intente mas tarde"
            })
        
        return render(request, "profile.html", {
                "message": "Mascota Registrada"
            })
        #return JsonResponse({"message": "Mascota register successfully."}, status=201)
    else:
        if propietario.is_provedor :
            provedor = Provedor.objects.get(provedor=propietario)
            return render(request, "profile.html", {"mascotas":mascotas, "provedor":provedor})
        else:
            return render(request, "profile.html", {"mascotas":mascotas, })
    

def dashboard(request):
    usuarios = CustomUser.objects.all()
    provedores = Provedor.objects.all()
    
    if request.method == "POST":
        pass
    else:
        if request.user.is_veterinario or request.user.is_provedor:
            return render ( request, "dashboard.html", {"provedores":provedores, "usuarios":usuarios} )
        else:
            return JsonResponse({"error": "No tienes privilegio para entrar aqui."}, status=404)
        
    
@csrf_exempt
def provedores(request):
    usuarios = CustomUser.objects.all()
    provedores = Provedor.objects.all()
    if request.method == "POST":
        nombre = request.POST["first_name"].capitalize()
        apellido = request.POST["last_name"].capitalize()
        dni = request.POST["dni"].capitalize()
        email = request.POST["email"]
        rut = request.POST["rut"]
        razonsocial = request.POST["razonSocial"]
        domicilio = request.POST["domicilio"]
        telefono = request.POST["telefono"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })
        

        # Attempt to create new User and Provedor for that user
        try:
            user = CustomUser.objects.create(
                dni=dni,
                first_name=nombre, 
                last_name=apellido, 
                email=email, 
                 
                
                )
            user.set_password(password)
            user.is_provedor = True
            user.save()
            provedor = Provedor.objects.create(
                provedor = user,
                rut = rut,
                domicilio = domicilio,
                telefono = telefono,
                razonSocial = razonsocial,
            )
            provedor.save()
        except IntegrityError:
            return render(request, "provedores.html", {
                "message": "Hubo un problema intente mas tarde"
            })
        
        return HttpResponseRedirect(reverse("provedores"))
    else:
        if request.user.is_veterinario or request.user.is_provedor:
            return render ( request, "provedores.html", {"provedores":provedores} )
        else:
            return JsonResponse({"error": "No tienes privilegio para entrar aqui."}, status=404)

@csrf_exempt
def productos(request):
    form = ProductoForm(request.POST)
    formCat = CategoryForm(request.POST)
    categorias = Category.objects.all()
    provedor = Provedor.objects.get(provedor=request.user.id)
    productos = Producto.objects.all()
    productosProvedor = Producto.objects.filter(vendedor=provedor)
    if request.method == 'POST':
        
        if form.is_valid():
            producto = form.save(commit=False)
            imagen = request.FILES.get('imagefile')
            producto.image = imagen
            producto.vendedor = provedor
            producto.save()
            return  HttpResponseRedirect(reverse("productos"))
        elif formCat.is_valid():
            formCat.save()
            return  HttpResponseRedirect(reverse("productos"))
        else:
                
            form = ProductoForm()
            formCat = CategoryForm()
            return render(request, "productos.html", {
                "form": form,
                "formCat" : formCat,
                "categorias": categorias,
                "productos": productos,
                
            })
    
    else:
        form = ProductoForm()
        formCat = CategoryForm()
        if request.user.is_veterinario :
            return render(request, "productos.html", {
            "form": form,
            "formCat" : formCat,
            "categorias": categorias,
            "productos": productos,
           
        })
        elif request.user.is_provedor:
            return render(request, "productos.html", {
            "form": form,
            "formCat" : formCat,
            "categorias": categorias,
            "productos": productosProvedor,
           
        })
        else:
            return JsonResponse({"error": "No tienes privilegio para entrar aqui."}, status=404)
        
    
    
@csrf_exempt
def usuarios(request):
    usuarios = CustomUser.objects.all()
    
    if request.method == "POST":
        nombre = request.POST["first_name"].capitalize()
        apellido = request.POST["last_name"].capitalize()
        dni = request.POST["dni"].capitalize()
        email = request.POST["email"]
        if request.POST.get('veterinario') == 'veterinario':
            
            veterinario = True
        else:
            veterinario = False
        
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })
        

        # Attempt to create new User and Provedor for that user
        try:
            user = CustomUser.objects.create(
                dni=dni,
                first_name=nombre, 
                last_name=apellido, 
                email=email, 
                 
                is_veterinario=veterinario
                )
            user.set_password(password)
            user.save()
            
        except IntegrityError:
            messages.warning(request, message= 'Hubo un problema intente mas tarde')
            
        
        return HttpResponseRedirect(reverse("usuarios"))
    else:
        if request.user.is_veterinario or request.user.is_provedor:
            return render ( request, "usuarios.html", {"usuarios":usuarios} )
        else:
            return JsonResponse({"error": "No tienes privilegio para entrar aqui."}, status=404)
        

@csrf_exempt
def editUser(request, id):
    
    try:
        user = CustomUser.objects.get(pk=id)
        
        if user.is_provedor:
            provedor = Provedor.objects.get(provedor=user)
        
    except CustomUser.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    if request.method == "GET":
        if user.is_provedor:
            return JsonResponse(provedor.serialize())
        else:
            
            return JsonResponse(user.serialize(), safe=False)
    elif request.method == "PUT":
        
        
        data = json.loads(request.body)
        if data.get("first_name") is not None:
                user.first_name = data["first_name"].capitalize()
        if data.get("last_name") is not None:
                user.last_name = data["last_name"].capitalize()
        if data.get("email") is not None:
                user.email = data["email"]      
        user.save()
        if user.is_provedor == True:
            if data.get("razonSocial") is not None:
                provedor.razonSocial = data["razonSocial"]
            if data.get("rut") is not None:
                provedor.rut = data["rut"]
            if data.get("domicilio") is not None:
                provedor.domicilio = data["domicilio"]
            if data.get("telefono") is not None:
                provedor.telefono = data["telefono"]   
            if data.get("email") is not None:
                provedor.provedor.email = data["email"]      
            
            
            provedor.save()    
        
        

        return JsonResponse({"message": "User register successfully."}, status=201)
        return HttpResponse(status=204)
        
    else:
        return render(request, "profile.html")   


@csrf_exempt
def reservas(request):
    now = datetime.datetime.now()
    formatted = now.strftime("%Y-%m-%d")
    # formatted = now.strftime("%Y-%m-%dT%H:%M")
    
    
    try:
        user = CustomUser.objects.get(pk=request.user.id)
        mascotas = Mascota.objects.filter(propietario=user)
    
    except user.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)
    if request.method == "GET":
        return render(request , "reservas.html", { "mascotas": mascotas, "formatted": formatted
                                                         
        })
    elif request.method == "POST":
             
        service = request.POST["servicio"]
        request_date = request.POST["dateselected"]
        request_h = request.POST["hr"]
        request_min = request.POST["min"]
        formatted_datetime = f'{request_date}T{request_h}:{request_min}'
        comment = request.POST["comment"]
        print(formatted_datetime)
        new_appointment = Appointment.objects.create(
            user = user,
            comment=comment,
            service=service,            
            datetime = formatted_datetime,
            email= user.email  ,
        )
        new_appointment.save()
        # calendar.create_event("Hola youtube","2024-04-15T15:30:00+02:00","2024-04-15T16:00:00+02:00","America/Argentina/Buenos_Aires",["elfabito@gmail.com"])
        
        # messages.success(request, message= 'Reserva registrada correctamente, espere que el veterinario apruebe su consulta')
        return HttpResponseRedirect(reverse("reservas"),{"message":messages.success(request, "Reserva registrada correctamente, espere que el veterinario apruebe su consulta")})
        # return JsonResponse({"msg": 'Register Successfully, wait for approved'}, status=404)
    
def deleteUser(request, id):
    try: 
        user = CustomUser.objects.get(pk=id)
        user.delete()
        
        return HttpResponseRedirect(reverse("usuarios"),{"message":messages.success(request, "Usuario eliminado")})
    except CustomUser.DoesNotExist:
        messages.error(request, "User no existe")
        return render(request, "usuarios.html")
    
def deleteProducto(request, id):
    try: 
        producto = Producto.objects.get(pk=id)
        producto.delete()
        
        return HttpResponseRedirect(reverse("productos"),{"message":messages.success(request, "Producto eliminado")})
    except CustomUser.DoesNotExist:
        messages.error(request, "Producto no existe")
        return render(request, "productos.html")
    
def deleteProvedor(request, id):


    try: 
        provedor = Provedor.objects.get(pk=id)
        provedor.delete()
        
        return HttpResponseRedirect(reverse("provedores"),{"message":messages.success(request, "Provedor eliminado")})
    except CustomUser.DoesNotExist:
        messages.error(request, "Provedor no existe")
        return render(request, "provedores.html")
    
def adminreservas(request):
    
    appointments = Appointment.objects.all().order_by('datetime')
    approved = appointments.filter(approved=True).count()
    canceled = appointments.filter(canceled=True).count()
    forapproved = appointments.count() - approved - canceled
    if request.method == "POST":
        pass
    else:
        if request.user.is_veterinario:
            return render ( request, "adminreservas.html", {"appointments":appointments, "count_approved":approved, "count_canceled": canceled,"count_forapproved":forapproved} )
        else:
            return JsonResponse({"error": "No tienes privilegio para entrar aqui."}, status=404)

@login_required
def editProducto(request, id):
    try:
        producto = Producto.objects.get(pk=id)
    except Producto.DoesNotExist:
        messages.error(request, "Producto no existe")
        return render(request, "productos.html")
    
    if request.method == "GET":
            return JsonResponse(producto.serialize())
    elif request.method == "PUT":
        data = json.loads(request.body)
        nombre = data.get("nombre")
        producto.nombre = nombre
        descripcion = data.get("descripcion")
        producto.descripcion = descripcion
        image = data.get("image")
        producto.image = image
        precio = data.get("precio")
        producto.precio = precio
        categoria = data.get("categoria")
        producto.categoria = categoria
        producto.save()
            
        return HttpResponseRedirect(reverse("productos"))



@login_required
@csrf_exempt
def reservaUser(request, id):
    try:
       
       appointment = Appointment.objects.get(pk=id)
   
    except Appointment.DoesNotExist:
        return JsonResponse({"error": "Appoint not found."}, status=404)
    if request.method == "GET":
        return JsonResponse(appointment.serialize())
    elif request.method == "PUT":
        data = json.loads(request.body)
        approved = data.get("approved")
        appointment.approved = approved
        canceled = data.get("canceled")
        appointment.canceled = canceled

        if appointment.approved:
            hora_y_media_despues =  appointment.datetime + datetime.timedelta(hours=1, minutes=30)
            print(hora_y_media_despues.strftime("%Y-%m-%dT%H:%M:%S%z"))
            print(appointment.datetime.strftime("%Y-%m-%dT%H:%M:%S%z"))
           
            calendar.create_event(f"Reserva con {appointment.user}",appointment.datetime.strftime("%Y-%m-%dT%H:%M:%S%z"), hora_y_media_despues.strftime("%Y-%m-%dT%H:%M:%S%z"),"America/Argentina/Buenos_Aires",["elfabito@gmail.com", f"{appointment.email}"])
            # calendar.create_event("Hola youtube","2024-04-15T15:30:00+02:00","2024-04-15T16:00:00+02:00","America/Argentina/Buenos_Aires",["elfabito@gmail.com"])
        appointment.save()
        
        return HttpResponseRedirect(reverse("reservas"))
        return HttpResponse(status=204)
    elif request.method == "DELETE":
        appointment.delete()
        # return HttpResponseRedirect(reverse("index"))
        return JsonResponse({"message": "Appoinment deleted successfully."}, status=201)