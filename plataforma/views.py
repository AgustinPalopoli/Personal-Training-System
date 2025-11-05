# Django core imports for rendering and auth
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect , JsonResponse
from django.shortcuts import render, redirect, reverse

# Local application models
from .models import User, Ejercicio, Peso,Rutina, Pizarron,Relacion_RyE,Relacion_PyR

# Authentication and permission decorators
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test

# Database queries and utilities
from django.db.models import F, Q
from datetime import datetime, timedelta
from django.contrib import messages

# File handling
import os
from django.core.files.storage import FileSystemStorage

# Other utilities
import random

# Custom utility functions
from . import util

# Landing page view
def inicio(request):
    """Renders the main landing page"""
    return render(request, "plataforma/inicio.html")

# Redirection view for general purpose redirects
def redireccion(request):
    """Renders the redirection page"""
    return render(request, "plataforma/redireccion.html")

# Superuser required for this view
@user_passes_test(lambda u: u.is_superuser)
def crear_cuentas(request):
    """
    Account creation view for superusers.
    Allows creating new users with different role permissions:
    - Admin
    - Regular User
    - Premium User
    """
    # Get content type for User model to manage permissions
    content_type = ContentType.objects.get_for_model(User)
    post_permission = Permission.objects.filter(content_type=content_type)
    # Extract specific role permissions
    for post in post_permission:
        string = str(post)
        if 'is_admin' in string:
            admin = post
        if 'is_user' in string:
            user = post
        if 'is_premiun' in string:
            premium = post
    if request.method == "POST":
        #Agarra informacion y valida
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["contrasena"]
        sexo = request.POST["sexo"]
        rol = request.POST["rol"]
        # Permissions
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            if rol == "admin":
                user.rol = 1
                user.user_permissions.add(admin)
            if rol == "user":
                user.rol = 2
                user.user_permissions.add(user)
            if rol == "premiun":
                user.rol = 3
                user.user_permissions.add(premium)
            user.save()
        except IntegrityError:
            return render(request, "plataforma/crear_cuentas.html", {
                "message": "Username already taken."
            })
        return HttpResponseRedirect(reverse("crear_cuentas"))
    else:
        return render(request, "plataforma/crear_cuentas.html")

def registrarse(request):
    """
    Public registration view.
    Handles new user registration with basic user permissions.
    Validates email uniqueness and password confirmation.
    """
    # Get user permission type
    content_type = ContentType.objects.get_for_model(User)
    post_permission = Permission.objects.filter(content_type=content_type)
    for post in post_permission:
        string = str(post)
        if 'is_user' in string:
            perm = post
    if request.method == "POST":
        usuario = request.POST["usuario"]
        email = request.POST["email"]
        sexo = request.POST["sexo"]
        contrasena = request.POST["contrasena"]
        confirmation = request.POST["contrasena_c"]
        if contrasena != confirmation:
            return render(request, "plataforma/crear_cuentas.html", {
                "message": "Passwords must match."
            })
        try:
            if not User.objects.filter(email=request.POST["email"]).exists():
                user = User.objects.create_user(usuario, email, contrasena)
                user.sexo = sexo
                user.rol = 2
                user.user_permissions.add(perm)
                user.save()
            else:
                messages.success(request, "Ya existe una cuenta creada con este email")
        except IntegrityError:
            messages.success(request, "Ya existe una cuenta creada con este nombre de usuario")
        return HttpResponseRedirect(reverse("redireccion"))


def iniciar_sesion(request):
    """
    Login view that handles user authentication.
    Redirects users to their appropriate dashboard based on their role:
    - Superuser: Account creation page
    - Admin: Admin dashboard
    - Regular User: User dashboard
    - Premium User: Premium dashboard
    """
    if request.method == "POST":
        # Attempt to authenticate user
        username = request.POST["usuario"]
        password = request.POST["contrasena"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponseRedirect(reverse("crear_cuentas"))
            if user.rol == 1:
                return HttpResponseRedirect(reverse("admin_inicio"))
            if user.rol == 2:
                return HttpResponseRedirect(reverse("usuario_g"))
            if user.rol == 3:
                return HttpResponseRedirect(reverse("usuario_inicio"))
        else:
            messages.success(request, "Usuario o contraseña incorrectos")
        return render(request, "plataforma/iniciar_sesion.html")
    else:
        return render(request, "plataforma/iniciar_sesion.html")



def salir(request):
    logout(request)
    return HttpResponseRedirect(reverse("inicio"))

@login_required
@permission_required('plataforma.ADMIN', raise_exception=True)
def admin_inicio(request):
    """
    Admin dashboard view.
    Displays all bulletin boards (pizarron) and handles their deletion.
    Requires admin permissions.
    """
    # Get all bulletin boards
    pizarron = Pizarron.objects.all()
    if request.method == "POST":
        # Handle deletion of selected bulletin boards
        ids = request.POST.getlist("eliminar")
        util.eliminar_modelo(Pizarron,ids)
    return render(request, "plataforma/admin_inicio.html",{"pizarron":pizarron})

@login_required
@permission_required('plataforma.ADMIN', raise_exception=True)
def admin_frases(request):
    if request.method == "GET":
        my_file = open("plataforma/static/plataforma/frases.txt", "r")
        data = my_file.read() 
        data_into_list = data.split("\n") 
        frase = random.choice(data_into_list)
        my_file.close() 
        return JsonResponse({'frase':frase})
    if request.method == "POST":
        os.remove("plataforma/static/plataforma/frases.txt")
        archivo = request.FILES["archivo"]
        fs = FileSystemStorage(location="plataforma/static/plataforma")  
        fs.save("frases.txt", archivo)
        return HttpResponse(status=204)


@login_required
@permission_required('plataforma.ADMIN', raise_exception=True)
def admin_pizarron_agregar(request):
    id_utilizados = list(Pizarron.objects.values_list("usuario", flat=True))
    usuarios = User.objects.filter(rol=3).exclude(id__in=id_utilizados)
    rutinas = Rutina.objects.filter(tipo_usuario="Premiun")
    if request.method == "POST":
        etiquetas = ["usuario","mensaje"]
        try:
            usuario = User.objects.get(id=request.POST["usuario"])
            data = [usuario,request.POST["mensaje"]]
            if not Pizarron.objects.filter(usuario = usuario ).exists() :
                pizarron = util.agregar_modelo(Pizarron,etiquetas,data)
                rutinas_selec = request.POST.getlist("rutinas_semana")
                etiquetas = ["pizarron_rutina","pizarron_id","orden"]
                for i in range(0,len(rutinas_selec)):
                    rutina = Rutina.objects.get(id=rutinas_selec[i])
                    data = [rutina,pizarron,i+1]
                    util.agregar_modelo(Relacion_PyR,etiquetas,data)
                    ejercicios = Relacion_RyE.objects.filter(rutina=rutina)
                    for j in range(0,len(ejercicios)):
                        if not usuario.pesos.filter(ejercicio = ejercicios[j].ej ).exists() :
                            if ejercicios[j].ej.peso_con_sin == "Con":
                                nuevo_peso = Peso(ejercicio=ejercicios[j].ej)
                                nuevo_peso.save()
                                usuario.pesos.add(nuevo_peso)
                                usuario.save()
            return HttpResponseRedirect(reverse("admin_inicio"))
        except:
            messages.success(request, "Error: no hay ningun usuario selecionado")
    return render(request, "plataforma/admin_pizarron_agregar.html",{"usuarios":usuarios,"rutinas":rutinas})

@login_required
@permission_required('plataforma.ADMIN', raise_exception=True)
def admin_pizarron_modificar(request,pizarron_id):
    pizarron = Pizarron.objects.get(id=pizarron_id)
    rutinas = Rutina.objects.filter(tipo_usuario="Premiun",tipo_sexo = pizarron.usuario.sexo)
    pizarron_rutinas = Relacion_PyR.objects.filter(pizarron_id=pizarron_id).order_by('orden')
    if request.method == "POST":
        etiquetas = ["usuario","mensaje"]
        data = [pizarron.usuario,request.POST["mensaje"]]
        pizarron = util.modificar_modelo(Pizarron,etiquetas,data,pizarron_id)
        rutinas_selec = request.POST.getlist("rutinas_semana")
        usuario = pizarron.usuario
        #NO TOCAR NO SE POR QUE MIERDA ESTO NO FUNCIONA CON EL UTIL.MODIFICAR MODELO PERO ASI SI FUNCIONA POR QUE?
        #QUIEN SABE. QUE ASCO DE VIDA
        for i in range(0,len(rutinas_selec)):
            A = Relacion_PyR.objects.get(id=pizarron_rutinas[i].id)
            B = Rutina.objects.get(id=rutinas_selec[i])
            setattr(A,"pizarron_rutina",B)
            A.save()
            rutina = Rutina.objects.get(id=rutinas_selec[i])
            ejercicios = Relacion_RyE.objects.filter(rutina=rutina)
            for j in range(0,len(ejercicios)):
                if not usuario.pesos.filter(ejercicio = ejercicios[j].ej ).exists() :
                    nuevo_peso = Peso(ejercicio=ejercicios[j].ej)
                    nuevo_peso.save()
                    usuario.pesos.add(nuevo_peso)
                    usuario.save()
        return HttpResponseRedirect(reverse("admin_inicio"))
    return render(request, "plataforma/admin_pizarron_modificar.html",{"pizarron":pizarron,"pizarron_rutinas":pizarron_rutinas,"rutinas":rutinas})

@login_required
@permission_required('plataforma.ADMIN', raise_exception=True)
def admin_ejercicio(request):
    """
    Exercise management view for admins.
    Displays all exercises and handles their deletion.
    Also manages associated images through custom utility function.
    """
    # Get all exercises
    ejercicios = Ejercicio.objects.all()
    if request.method == "POST":
        # Handle deletion of selected exercises and their images
        ids = request.POST.getlist("eliminar")
        util.eliminar_modelo_imagen(Ejercicio,ids)
    return render(request, "plataforma/admin_ejercicio.html",{"ejercicios":ejercicios})

@login_required
@permission_required('plataforma.ADMIN', raise_exception=True)
def admin_ejercicio_agregar(request):
    if request.method == "POST":
        etiquetas = ["tipo","grupo_muscular","nombre_ej","series","repeticiones","descanso","peso_con_sin","imagen"]
        if "imagen" in request.FILES:
            if not Ejercicio.objects.filter(tipo=util.at(request.POST["tipo"])).filter(grupo_muscular=util.at(request.POST["grupo_muscular"])).filter(nombre_ej=util.at(request.POST["nombre_ej"])):
                descanso = timedelta(minutes = int(request.POST["minutos"]), seconds = int(request.POST["segundos"]))
                data = [request.POST["tipo"],request.POST["grupo_muscular"],request.POST["nombre_ej"],request.POST["series"],request.POST["repeticiones"],descanso,request.POST["peso_con_sin"],request.FILES["imagen"]]
                util.agregar_modelo(Ejercicio,etiquetas,data)
                messages.success(request, "Los valores fueron guardados correctamente :)")
                return render(request, "plataforma/admin_ejercicio_agregar.html")
            else:
                messages.success(request, "ERROR: Ya existe un ejercicio con este tipo, grupo muscular y nombre")
                return render(request, "plataforma/admin_ejercicio_agregar.html")
        else:
            messages.success(request, "ERROR: Falto la imagen señor movimiento")
            return render(request, "plataforma/admin_ejercicio_agregar.html")
    return render(request, "plataforma/admin_ejercicio_agregar.html")


@login_required
@permission_required('plataforma.ADMIN', raise_exception=True)
def admin_ejercicio_modificar(request,ejercicio_id):
    ejercicio = Ejercicio.objects.get(id=ejercicio_id)
    if request.method == "POST":
        etiquetas = ["tipo","grupo_muscular","nombre_ej","series","repeticiones","descanso","peso_con_sin","imagen"]
        descanso = timedelta(minutes = int(request.POST["minutos"]), seconds = int(request.POST["segundos"]))
        data = [request.POST["tipo"],request.POST["grupo_muscular"],request.POST["nombre_ej"],request.POST["series"],request.POST["repeticiones"],descanso,request.POST["peso_con_sin"]]
        if not Ejercicio.objects.filter(tipo=util.at(request.POST["tipo"])).filter(grupo_muscular=util.at(request.POST["grupo_muscular"])).filter(nombre_ej=util.at(request.POST["nombre_ej"])):
            if "imagen" in request.FILES:
                data.append(request.FILES["imagen"])
                util.modificar_modelo_imagen(Ejercicio,etiquetas,data,ejercicio_id)
                return HttpResponseRedirect(reverse("admin_ejercicio"))
            else:
                util.modificar_modelo(Ejercicio,etiquetas,data,ejercicio_id)
                return HttpResponseRedirect(reverse("admin_ejercicio"))
        else:
            messages.success(request, "ERROR: Ya existe un ejercicio con este tipo, grupo muscular y nombre")
            return render(request, "plataforma/admin_ejercicio_modificar.html",{"ejercicio":ejercicio})
    return render(request, "plataforma/admin_ejercicio_modificar.html",{"ejercicio":ejercicio})


@login_required
@permission_required('plataforma.ADMIN', raise_exception=True)
def admin_rutina(request):
    rutinas = Rutina.objects.all()
    if request.method == "POST":
        ids = request.POST.getlist("eliminar")
        util.eliminar_modelo(Rutina,ids)
    return render(request, "plataforma/admin_rutina.html",{"rutinas":rutinas})


@login_required
@permission_required('plataforma.ADMIN', raise_exception=True)
def admin_rutina_agregar(request):
    ejercicios = Ejercicio.objects.all()
    if request.method == "POST":
        if not Rutina.objects.filter(nombre_rutina = util.at(request.POST["nombre_rutina"])):
            etiquetas = ["nombre_rutina","tipo_usuario","tipo_sexo"]
            data = [request.POST["nombre_rutina"],request.POST["tipo_usuario"],request.POST["tipo_sexo"]]
            rutina = util.agregar_modelo(Rutina,etiquetas,data)
            ejercicios = request.POST.getlist("todos_ejercicios")
            etiquetas = ["rutina","ej","orden"]
            for i in range(0,len(ejercicios)):
                ej = Ejercicio.objects.get(id=ejercicios[i])
                data = [rutina,ej,i+1]
                util.agregar_modelo(Relacion_RyE,etiquetas,data)
            return HttpResponseRedirect(reverse("admin_rutina"))
        else:
            messages.success(request, "ERROR: Ya existe una rutina con este nombre")
            return render(request, "plataforma/admin_rutina_agregar.html",{"ejercicios":ejercicios})
    return render(request, "plataforma/admin_rutina_agregar.html",{"ejercicios":ejercicios})


@login_required
@permission_required('plataforma.ADMIN', raise_exception=True)
def admin_rutina_modificar(request,rutina_id):
    ejercicios = Ejercicio.objects.all()
    rutinas = Relacion_RyE.objects.filter(rutina=rutina_id)
    if request.method == "POST":
        if not Rutina.objects.filter(nombre_rutina = util.at(request.POST["nombre_rutina"])):    
            etiquetas = ["nombre_rutina","tipo_usuario","tipo_sexo"]
            data = [request.POST["nombre_rutina"],request.POST["tipo_usuario"],request.POST["tipo_sexo"]]
            rutina = util.modificar_modelo(Rutina,etiquetas,data,rutina_id)
            ejercicios = request.POST.getlist("todos_ejercicios")
            etiquetas = ["rutina","ej","orden"]
            for i in range(0,len(rutinas)):
                ej = Ejercicio.objects.get(id=ejercicios[i])
                data = [rutina,ej,i+1]
                util.modificar_modelo(Relacion_RyE,etiquetas,data,rutinas[i].id)
                x = i
            x += 2
            if len(rutinas)<(len(ejercicios)-1):
                for j in range(x,len(ejercicios)):
                    ej = Ejercicio.objects.get(id=ejercicios[j])
                    data = [rutina,ej,j]
                    util.agregar_modelo(Relacion_RyE,etiquetas,data)
            return HttpResponseRedirect(reverse("admin_rutina"))
        else:
            messages.success(request, "ERROR: Ya existe una rutina con este nombre")
            return render(request, "plataforma/admin_rutina_modificar.html",{"ejercicios":ejercicios,"rutinas":rutinas})
    return render(request, "plataforma/admin_rutina_modificar.html",{"ejercicios":ejercicios,"rutinas":rutinas})


@login_required
@permission_required('plataforma.ADMIN', raise_exception=True)
def admin_rutina_ver(request,rutina_id):
    rutinas = Relacion_RyE.objects.filter(rutina=rutina_id)
    return render(request, "plataforma/admin_rutina_ver.html",{"rutinas":rutinas})


@login_required
@permission_required('plataforma.ADMIN', raise_exception=True)
def admin_usuarios(request):
    usuarios = User.objects.filter(~Q(rol=1))
    if request.method == "POST":
        ids = request.POST.getlist("eliminar")
        util.eliminar_modelo(User,ids)
    return render(request, "plataforma/admin_usuarios.html",{"usuarios":usuarios})


@login_required
@permission_required('plataforma.ADMIN', raise_exception=True)
def admin_usuarios_agregar(request):
    if request.method == "POST":
        if not User.objects.filter(email=request.POST["email"]).exists():
            try: 
                usuario = User.objects.create_user(username=request.POST["username"], email=request.POST["email"], password=request.POST["password"],sexo=request.POST["sexo"],rol=request.POST["rol"])
                content_type = ContentType.objects.get_for_model(User)
                post_permission = Permission.objects.filter(content_type=content_type)
                for post in post_permission:
                    string = str(post)
                    if 'is_user' in string:
                        user = post
                    if 'is_premiun' in string:
                        premium = post
                if request.POST["rol"] == "2":
                    usuario.user_permissions.add(user)
                else:
                    usuario.user_permissions.add(premium)
                usuario.save()
                return HttpResponseRedirect(reverse("admin_usuarios"))
            except:
                messages.success(request, "ERROR: Ya existe un usuario con este nombre")
                return render(request, "plataforma/admin_usuarios_agregar.html")
        else:
            messages.success(request, "ERROR: Ya existe un usuario con este mail")
            return render(request, "plataforma/admin_usuarios_agregar.html")
    return render(request, "plataforma/admin_usuarios_agregar.html")


@login_required
@permission_required('plataforma.ADMIN', raise_exception=True)
def admin_usuarios_CambiarContrasena(request,usuario_id):
    usuario = User.objects.get(id=usuario_id)
    if request.method == "POST":
        usuario.password = request.POST["password"]
        return HttpResponseRedirect(reverse("admin_usuarios"))
    return render(request, "plataforma/admin_usuarios_CambiarContrasena.html",{"usuario":usuario})


@login_required
@permission_required('plataforma.ADMIN', raise_exception=True)
def admin_usuario_premiun(request,usuario_id):
    if request.method == "GET":
        usuario = User.objects.get(id=usuario_id)
        usuario.rol = 3
        content_type = ContentType.objects.get_for_model(User)
        post_permission = Permission.objects.filter(content_type=content_type)
        for post in post_permission:
            string = str(post)
            if 'is_user' in string:
                user = post
            if 'is_premiun' in string:
                premium = post
        usuario.user_permissions.remove(user)
        usuario.user_permissions.add(premium)
        usuario.save()
    return HttpResponseRedirect(reverse("admin_usuarios"))

def pesos(request,usuario):
    cantidad_peso = request.POST.getlist("cantidad_peso")
    i = 0
    for ex in usuario.pesos.all():
        ex.cantidad_peso = cantidad_peso[i]
        i += 1
        ex.save()
    usuario.save()


@login_required
@permission_required('plataforma.ADMIN', raise_exception=True)
def admin_usuarios_pesos(request,usuario_id):
    usuario = User.objects.get(id=usuario_id)
    if request.method == "POST":
        pesos(request,usuario)
    return render(request, "plataforma/admin_usuarios_pesos.html",{"usuario":usuario})

@login_required
@permission_required('plataforma.PREMIUN', raise_exception=True)
def usuario_inicio(request):
    """
    Premium user dashboard view.
    Shows user's assigned routines and bulletin board messages.
    Requires premium user permissions.
    """
    # Get current user
    usuario = request.user
    try:
        # Get user's bulletin board and associated routines
        pizarron = Pizarron.objects.get(usuario=usuario)
        rutinas = Relacion_PyR.objects.filter(pizarron_id=pizarron)
        # Display any messages from the bulletin board
        if pizarron.mensaje:
            messages.success(request, pizarron.mensaje)
    except:
        # If no bulletin board exists, show empty routine list
        rutinas = []
    return render(request, "plataforma/usuario_inicio.html",{"rutinas":rutinas})

@login_required
@permission_required('plataforma.PREMIUN', raise_exception=True)
def usuario_rutina(request,rutina_id):
    """
    Premium user routine detail view.
    Shows exercises in a specific routine and manages user's weights for each exercise.
    Handles both viewing and updating exercise weights.
    """
    # Get current user
    usuario = request.user
    if request.method == "GET":
        # Get routine details and exercises ordered by sequence
        id_r = rutina_id
        rutina = Relacion_RyE.objects.filter(rutina=rutina_id).order_by("orden")
        datos = []
        for item in rutina:
            pesos = []
            pesos.append(item)
            try:
                pesos.append(usuario.pesos.get(ejercicio=item.ej))
            except:
                pesos.append("")
            datos.append(pesos)
        return render(request, "plataforma/usuario_rutina.html",{"rutina":rutina,"datos":datos,"id_r":id_r})
    if request.method == "POST":
        cantidad_peso = request.POST.getlist("cantidad_peso")
        ejercicio = request.POST.getlist("ejercicio_id")
        for i in range(0,len(cantidad_peso)):
            cambiar = Peso.objects.get(id = usuario.pesos.get(ejercicio=ejercicio[i]).id)
            cambiar.cantidad_peso = cantidad_peso[i]
            cambiar.save()
        return HttpResponse(status=204)

@login_required
@permission_required('plataforma.PREMIUN', raise_exception=True)
def usuario_peso(request):
    usuario = request.user
    if request.method == "POST":
        pesos(request,usuario)
        messages.success(request, "Los valores fueron guardados correctamente")
    try:
        datos = usuario.pesos.all()
    except:
        datos = []
    return render(request, "plataforma/usuario_peso.html",{"usuario":usuario,"datos":datos})

@login_required
@permission_required('plataforma.PREMIUN', raise_exception=True)
def usuario_estiramientos(request):
    estiramiento = Ejercicio.objects.filter(tipo="Estiramiento")
    return render(request, "plataforma/usuario_estiramientos.html",{"estiramiento":estiramiento})

@login_required
@permission_required('plataforma.USER', raise_exception=True)
def usuario_g(request):
    """
    Free user dashboard view.
    Shows available free routines filtered by user's gender.
    Requires basic user permissions.
    """
    usuario = request.user
    # Get free routines matching user's gender
    rutinas = Rutina.objects.filter(tipo_usuario="Gratis",tipo_sexo=usuario.sexo)
    return render(request, "plataforma/usuario_g.html",{"rutinas":rutinas})

@login_required
@permission_required('plataforma.USER', raise_exception=True)
def usuario_g_rutinas(request,rutina_id):
    """
    Free user routine detail view.
    Shows exercises in a specific free routine.
    Does not include weight tracking functionality.
    """
    # Get routine exercises ordered by sequence
    rutina = Relacion_RyE.objects.filter(rutina=rutina_id).order_by("orden")
    return render(request, "plataforma/usuario_g_rutinas.html",{"rutina":rutina})

@login_required
@permission_required('plataforma.USER', raise_exception=True)
def usuario_g_premiun(request):
    return render(request, "plataforma/usuario_g_premiun.html")

