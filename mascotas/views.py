from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.db import IntegrityError
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.contrib import messages
import json
from google_calendar_class import *
import datetime
from django.views import View
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import paypalrestsdk
from .Carrito import *
from django.core.mail import send_mail
from django.conf import settings
from .utils import render_to_pdf
from django.utils import timezone





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
            messages.warning(request=request,message="We have a user register with that dni")
            return HttpResponseRedirect(reverse("register"))
            # return render(request, "register.html", {
            #     "message": "We have a user register with that dni"
            # })
        login(request, user)
        return HttpResponseRedirect(reverse("home"))
       
    else:
        return render(request, "register.html")
    
@csrf_exempt
def profile(request):
    datetimenow = timezone.now()
    propietario = CustomUser.objects.get(pk=request.user.id) 
    
    appforapproved = Appointment.objects.filter(approved=False,canceled=False, user=request.user,datetime_ordered__gte=datetimenow).order_by('datetime_ordered')
    appapproved = Appointment.objects.filter(approved=True, user=request.user,datetime_ordered__gte=datetimenow).order_by('datetime_ordered')
    appcanceled = Appointment.objects.filter(canceled=True, user=request.user).order_by('datetime_ordered')
    approved =  appapproved.count()
    canceled = appcanceled.count()
    forapproved = appforapproved.count()
    mascotas = Mascota.objects.filter(propietario=propietario)
    
    appointments_pass = Appointment.objects.filter(user=request.user,datetime_ordered__lt=datetimenow).order_by('datetime_ordered')
    passcount = Appointment.objects.filter(user=request.user,datetime_ordered__lt=datetimenow).count()
    
    if request.method == "POST":
                
         
        nombre = request.POST["nombre"].capitalize()
        especie = request.POST["especie"].capitalize()
        raza = request.POST["raza"].capitalize()
        edad = request.POST["edad"]
        fechaNac = request.POST["fechaNac"]
        image = request.FILES.get('imagefile')
        
        

        # Attempt to create new Mascota
        try:
            mascota = Mascota.objects.create(
                nombre=nombre,
                especie=especie, 
                raza=raza, 
                edad=edad, 
                fechaNac=fechaNac, 
                image= image,
                propietario = propietario
                )
           
            mascota.save()
            

        except IntegrityError:
            messages.warning(request=request,message="Hubo un problema intente mas tarde")
            return HttpResponseRedirect(reverse("profile"))
        
        messages.success(request=request,message="Mascota registrada correctamente")
        return HttpResponseRedirect(reverse("profile"))
       
    else:
        if propietario.is_provedor :
            provedor = Provedor.objects.get(provedor=propietario)
            return render(request, "profile.html", {"mascotas":mascotas, "provedor":provedor} )
        else:
            return render(request, "profile.html", {"passcount":passcount,"datetimenow":datetimenow,"appointments_pass":appointments_pass,"mascotas":mascotas,"appforapproved":appforapproved,"appapproved": appapproved, "appcanceled":appcanceled, "count_approved":approved, "count_canceled": canceled,"count_forapproved":forapproved})
    

def dashboard(request):
    datetimenow = timezone.now()
    #Ultimos 3 usuarios, provedores , reservas y productos 
    usuarios = CustomUser.objects.filter(is_veterinario=False, is_provedor=False).order_by('-id')[:3]
    provedores = Provedor.objects.order_by('-idProvedor')[:3]
    productos =  Producto.objects.order_by('-idProducto')[:3]
    
    appapproved = Appointment.objects.filter(approved=True,datetime_ordered__gte=datetimenow).order_by('datetime_ordered')[:3]
    appforapproved = Appointment.objects.filter(approved=False,canceled=False,datetime_ordered__gte=datetimenow).order_by('datetime_ordered')[:3]
    datetimenow = datetime.datetime.now()
    if request.method == "POST":
        pass
    else:
        if request.user.is_veterinario or request.user.is_provedor:
            return render ( request, "adminPanel/dashboard_home.html", {"provedores":provedores, "usuarios":usuarios, "productos": productos, "appapproved" : appapproved, "appforapproved": appforapproved, "datetimenow" : datetimenow} )
        else:
            return JsonResponse({"error": "No tienes privilegio para entrar aqui."}, status=404)
        
    
@csrf_exempt
def provedores(request):
  
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
            return HttpResponseRedirect(reverse("provedores"),{"message":messages.warning(request, message= 'Hubo un problema intente mas tarde')})
        return HttpResponseRedirect(reverse("provedores"),{"message":messages.success(request, "Provedor creado con exito")})
    else:
        if request.user.is_veterinario or request.user.is_provedor:
            return render ( request, "adminPanel/provedores.html", {"provedores":provedores} )
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
            return render(request, "adminPanel/productos.html", {
                "form": form,
                "formCat" : formCat,
                "categorias": categorias,
                "productos": productos,
                
            })
    
    else:
        form = ProductoForm()
        formCat = CategoryForm()
        if request.user.is_veterinario :
            return render(request, "adminPanel/productos.html", {
            "form": form,
            "formCat" : formCat,
            "categorias": categorias,
            "productos": productos,
           
        })
        elif request.user.is_provedor:
            return render(request, "adminPanel/productos.html", {
            "form": form,
            "formCat" : formCat,
            "categorias": categorias,
            "productos": productosProvedor,
           
        })
        else:
            return JsonResponse({"error": "No tienes privilegio para entrar aqui."}, status=404)
        
   
class ListUsuariosPdf(View):
    def get(self,request, *args, **kwargs):
        usuarios = CustomUser.objects.all()
        data = {
            'usuarios' : usuarios
        }
        pdf = render_to_pdf('pdf/usuarios_pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

        
class ListProductsPdf(View):
    def get(self,request, *args, **kwargs):
        productos = Producto.objects.all()
        data = {
            'productos' : productos
        }
        pdf = render_to_pdf('pdf/productos_pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

class ListProvedoresPdf(View):
    def get(self,request, *args, **kwargs):
        provedores = Provedor.objects.all()
        data = {
            'provedores' : provedores
        }
        pdf = render_to_pdf('pdf/provedores_pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
     
class ListReservasPdf(View):
    def get(self,request, *args, **kwargs):
        datetimenow = timezone.now()
        
        appforapproved = Appointment.objects.filter(approved=False,canceled=False,datetime_ordered__gte=datetimenow).order_by('datetime_ordered')
        appapproved = Appointment.objects.filter(approved=True,datetime_ordered__gte=datetimenow).order_by('datetime_ordered')
        
        appcanceled = Appointment.objects.filter(canceled=True).order_by('datetime_ordered')
        
        appointments_pass = Appointment.objects.filter(datetime_ordered__lt=datetimenow).order_by('datetime_ordered')
        
        data = {
            'appointments_pass' : appointments_pass,
            'appapproved' : appapproved,
            'appcanceled' : appcanceled,
            'appforapproved' : appforapproved
        }
        pdf = render_to_pdf('pdf/reservas_pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


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
            
            return HttpResponseRedirect(reverse("usuarios"),{"message":messages.warning(request, message= 'Hubo un problema intente mas tarde')})
        return HttpResponseRedirect(reverse("usuarios"),{"message":messages.success(request, "Reserva registrada correctamente, espere que el veterinario apruebe su consulta")})
        
    else:
        if request.user.is_veterinario or request.user.is_provedor:
            return render ( request, "adminPanel/usuarios.html", {"usuarios":usuarios} )
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
        servicios = Service.objects.all()
        veterinarios = CustomUser.objects.filter(is_veterinario=True)
        user = CustomUser.objects.get(pk=request.user.id)
        mascotas = Mascota.objects.filter(propietario=user)
    
    except user.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)
    if request.method == "GET":
        return render(request , "reservas.html", {"servicios":servicios, "mascotas": mascotas, "formatted": formatted
                                                         
        })
    elif request.method == "POST":
             
        service = request.POST["servicio"]
        service_obj = Service.objects.get(name=service)
        request_date = request.POST["dateselected"]
        request_h = request.POST["hr"]
        request_min = request.POST["min"]
        formatted_datetime = f'{request_date}T{request_h}:{request_min}'
        comment = request.POST["comment"]
        print(formatted_datetime)
        new_appointment = Appointment.objects.create(
            user = user,
            comment=comment,
            service=service_obj,            
            datetime_ordered = formatted_datetime,
            
        )
        recipients = [user.email]
        for veterinario in veterinarios:
            recipients.append(veterinario.email)
        send_mail(
    		subject=f'Nueva reserva de {user.first_name} esperando por aprobar',
    		message=comment,
    		from_email=settings.EMAIL_HOST_USER,
    		recipient_list=recipients)
        new_appointment.save()
       
        return HttpResponseRedirect(reverse("reservas"),{"message":messages.success(request, "Reserva registrada correctamente, espere que el veterinario apruebe su consulta")})


def allCat(request):
    categorias = Category.objects.all()
    return JsonResponse([categoria.serialize() for categoria in categorias], safe=False)

def deleteServicio(request,id):
    try:
        servicio = Service.objects.get(pk=id)
        servicio.delete()
        return HttpResponseRedirect(reverse("adminreservas"),{"message":messages.success(request, "Servicio eliminado")})
    except Category.DoesNotExist:
        messages.error(request, "Servicio no existe")
        return render(request, "adminPanel/reservas_control.html")
def deleteMascota(request,id):
    try:
        mascota = Mascota.objects.get(pk=id)
        mascota.delete()
        return HttpResponseRedirect(reverse("profile"),{"message":messages.success(request, "Mascota eliminada")})
    except Category.DoesNotExist:
        messages.error(request, "Mascota no existe")
        return render(request, "profile.html")

def deleteCat(request,id):
    try:
        category = Category.objects.get(pk=id)
        category.delete()
        return HttpResponseRedirect(reverse("productos"),{"message":messages.success(request, "Categoria eliminada")})
    except Category.DoesNotExist:
        messages.error(request, "Categoria no existe")
        return render(request, "productos.html")
def deleteUser(request, id):
    try: 
        user = CustomUser.objects.get(pk=id)
        user.delete()
        
        return HttpResponseRedirect(reverse("usuarios"),{"message":messages.success(request, "Usuario eliminado")})
    except CustomUser.DoesNotExist:
        messages.error(request, "User no existe")
        return render(request, "adminPanel/usuarios.html")
    
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
    datetimenow = timezone.now()
    
    appforapproved = Appointment.objects.filter(approved=False,canceled=False,datetime_ordered__gte=datetimenow).order_by('datetime_ordered')
    appapproved = Appointment.objects.filter(approved=True,datetime_ordered__gte=datetimenow).order_by('datetime_ordered')
    appcanceled = Appointment.objects.filter(canceled=True).order_by('datetime_ordered')
    approved = appapproved.count()
    canceled = appcanceled.count()
    forapproved = appforapproved.count()
    formService = ServiceForm()
    servicios = Service.objects.all()
    
    appointments_pass = Appointment.objects.filter(datetime_ordered__lt=datetimenow).order_by('datetime_ordered')
    passcount = Appointment.objects.filter(datetime_ordered__lt=datetimenow).count()
    
    if request.method == "POST":
        nombre = request.POST["name"]
        precio = request.POST["precio"]
        try:
            service = Service.objects.create(
                name=nombre,
                precio=precio, 
                )
            service.save()           
        except IntegrityError:
            return HttpResponseRedirect(reverse("adminreservas"),{"message":messages.warning(request, message= 'Hubo un problema intente mas tarde')})
        return HttpResponseRedirect(reverse("adminreservas"),{"message":messages.success(request, "Servicio creado correctamente")})
    else:
        if request.user.is_veterinario:
            return render ( request, "adminPanel/reservas_control.html", {"datetimenow":datetimenow,"passcount":passcount,"appointments_pass":appointments_pass,"servicios":servicios,"formService":formService,"appforapproved":appforapproved,"appapproved": appapproved, "appcanceled":appcanceled, "count_approved":approved, "count_canceled": canceled,"count_forapproved":forapproved} )
        else:
            return JsonResponse({"error": "No tienes privilegio para entrar aqui."}, status=404)

@login_required
@csrf_exempt
def editProducto(request, id):
    try:

        producto = Producto.objects.get(pk=id)
        total = 0
        if request.user.is_authenticated:
            if "carrito" in request.session.keys():
                for key, value in request.session["carrito"].items():
                    total += int(value["precio"])
        
    except Producto.DoesNotExist:
        messages.error(request, "Producto no existe")
        return render(request, "productos.html")
    
    if request.method == "GET":
           return render ( request, "product_detail.html", { "total_carrito": total,"producto": producto, "stripe_publishable_key" : settings.STRIPE_PUBLIC_KEY })
    elif request.method == "PUT":
        data = json.loads(request.body)
        nombre = data.get("nombre")
        if nombre is not None:
           producto.nombre = nombre
        descripcion = data.get("descripcion")
        if descripcion is not None:
            producto.descripcion = descripcion
        image = data.get("image")
        if image is not None:
            producto.image = image
        precio = data.get("precio")
        if precio is not None:        
            producto.precio = precio
        categoria_text = data.get("categoria")
        if categoria_text is not None:
            categoria = Category.objects.get(name=categoria_text)
            producto.categoria = categoria
        cantidad = data.get("cantidad")
        if cantidad is not None:
            producto.cantidad = cantidad
        producto.save()
            
        return HttpResponseRedirect(reverse("productos"))
    
@login_required  
def productosList(request):
    
    total = 0
    if request.user.is_authenticated:
        if "carrito" in request.session.keys():
            for key, value in request.session["carrito"].items():
                total += int(value["precio"])
    productos = Producto.objects.all().order_by('date')        
    return render(request, 'productos_list.html',{ "total_carrito": total,"productos": productos,  "stripe_publishable_key" : settings.STRIPE_PUBLIC_KEY  })      
       

@login_required
@csrf_exempt
def reservaUser(request, id):
    try:
       veterinarios = CustomUser.objects.filter(is_veterinario=True)
       appointment = Appointment.objects.get(pk=id)
       recipients = [appointment.user.email]
    #    recipients_mails = ",".join(recipients)
       for veterinario in veterinarios:
           recipients.append(veterinario.email)
    except Appointment.DoesNotExist:
        return JsonResponse({"error": "Appoint not found."}, status=404)
    if request.method == "GET":
        return JsonResponse(appointment.serialize())
    elif request.method == "PUT":
        data = json.loads(request.body)
        approved = data.get("approved")
        if approved is not None:
            appointment.approved = approved
        canceled = data.get("canceled")
        if canceled is not None:
            appointment.canceled = canceled
        appointment.save()
        
        if appointment.approved:
            hora_y_media_despues =  appointment.datetime_ordered + datetime.timedelta(hours=1, minutes=30)
            print(hora_y_media_despues.strftime("%Y-%m-%dT%H:%M:%S%z"))
            print(appointment.datetime_ordered.strftime("%Y-%m-%dT%H:%M:%S%z"))

            #Crea Evento de GOOGLE Calendar cuando se aprueba la reserva
            calendar.create_event(f"Reserva con {appointment.user}",
                                  appointment.datetime_ordered.strftime("%Y-%m-%dT%H:%M:%S%z"),
                                  hora_y_media_despues.strftime("%Y-%m-%dT%H:%M:%S%z"),
                                  "America/Argentina/Buenos_Aires",recipients)
            
            send_mail(
    		subject=f'Reserva realizada con exito! de {appointment.user.first_name} ...esperando por el pago',
    		message="Realize el pago por favor, comuniquese a la brevedad",
    		from_email=settings.EMAIL_HOST_USER,
    		recipient_list= recipients)
            # calendar.create_event("Hola ","2024-04-15T15:30:00+02:00","2024-04-15T16:00:00+02:00","America/Argentina/Buenos_Aires",["example@gmail.com"])
            return HttpResponseRedirect(reverse("reservas"),{"message":messages.success(request, "Reserva aprobada con exito")})
        elif appointment.canceled:

            return HttpResponseRedirect(reverse("reservas"),{"message":messages.error(request, "Reserva cancelada")})
    
    elif request.method == "DELETE":
        appointment.delete()
        
        return HttpResponseRedirect(reverse("reservas"),{"message":messages.error(request, "Reserva eliminada")})

# PAYMENT STRIPE
@login_required
@csrf_exempt
def create_checkout_session(request, id):
    
    producto = Producto.objects.get(idProducto=id)
    user = CustomUser.objects.get(id= request.user.id)
    stripe.api_key = settings.STRIPE_SECRET_KEY 

    checkout_session = stripe.checkout.Session.create(
            customer_email = user.email,
            payment_method_types = ['card'],
            line_items=[
                {
                    'price_data':{
                        'currency': 'USD',
                        'product_data': {
                            'name': producto.nombre
                        },
                        'unit_amount': int(producto.precio * 100)
                    },
                    'quantity': 1
                }
            ],
            mode= 'payment',
        
            success_url= request.build_absolute_uri(reverse("payment_success",args=[producto.idProducto])) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse("failed",args=[producto.idProducto])) + "?session_id={CHECKOUT_SESSION_ID}",
            )
    return JsonResponse({"sessionId": checkout_session.id})

# PAYMENT STRIPE CARRITO
@login_required
@csrf_exempt
def create_checkout_session_carrito(request):
    carrito = Carrito(request)
    
    user = CustomUser.objects.get(id= request.user.id)
    stripe.api_key = settings.STRIPE_SECRET_KEY 

    checkout_session = stripe.checkout.Session.create(
            customer_email = user.email,
            payment_method_types = ['card'],
            line_items=[
                {
                    'price_data':{
                        'currency': 'USD',
                        'product_data': {
                            'name': "Total Carrito"
                        },
                        'unit_amount': int((carrito.totalCarrito(request)) * 100)
                    },
                    'quantity': 1
                }
            ],
            mode= 'payment',
        
            success_url= request.build_absolute_uri(reverse("payment_success_carrito")) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse("payment_failed_carrito")) + "?session_id={CHECKOUT_SESSION_ID}",
            )
    return JsonResponse({"sessionId": checkout_session.id})

def payment_success(request, id):
  return(request, 'payment_success.html')
 
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET,
})

#PAYMENT PAYPAL
def create_payment(request, id):
    producto = Producto.objects.get(pk=id)
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal",
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('execute_payment')),
            "cancel_url": request.build_absolute_uri(reverse('payment_failed')),
        },
        "transactions": [
            {
                "amount": {
                    "total": ('%.2f' % producto.precio),  # Total amount in USD
                    "currency": "USD",
                },
                "description": producto.nombre,
            }
        ],
    })

    if payment.create():
        return redirect(payment.links[1].href)  # Redirect to PayPal for payment
    else:
        return render(request, 'payment_failed.html')

@login_required
#PAYMENT PAYPAL CARRITO
def create_payment_carrito(request):
    
    carrito = Carrito(request)
    
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal",
        },
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('execute_payment')),
            "cancel_url": request.build_absolute_uri(reverse('payment_failed_carrito')),
        },
        "transactions": [
            {
                "amount": {
                    "total": ('%.2f' % carrito.totalCarrito(request)),  # Total amount in USD
                    "currency": "USD",
                },
                "description": str(carrito.showproductos()),
            }
        ],
    })

    if payment.create():
        return redirect(payment.links[1].href)  # Redirect to PayPal for payment
    else:
        return render(request, 'payment_failed.html')

def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return render(request, 'payment_success.html')
    else:
        return render(request, 'payment_failed.html')

def payment_failed(request):
    return render(request, 'payment_failed.html')

# CARRITO de Compras

def agregar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(idProducto=producto_id)
    carrito.agregarProducto(producto)
    return redirect("productosList")

def eliminar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(idProducto=producto_id)
    carrito.eliminarProducto(producto)
    return redirect("productosList")

def restar_producto(request, producto_id):
    carrito = Carrito(request)
    producto = Producto.objects.get(idProducto=producto_id)
    carrito.restarProducto(producto)
    return redirect("productdetail", producto_id)

def limpiar_carrito(request):
    carrito = Carrito(request)
    carrito.limpiarCarrito()
    return redirect("productosList")

def total_carrito(request):
    total = 0
    if request.user.is_authenticated:
        if "carrito" in request.session.keys():
            for key, value in request.session["carrito"].items():
                total += int(value["precio"])
    return {"total_carrito": total}