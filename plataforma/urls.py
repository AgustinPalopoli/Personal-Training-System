from django.urls import path

from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    #Base
    path("", views.inicio, name="inicio"),
    path("redireccion", views.redireccion, name="redireccion"),
    path("crear_cuentas", views.crear_cuentas, name="crear_cuentas"),
    path("registrarse", views.registrarse, name="registrarse"),
    path("iniciar_sesion", views.iniciar_sesion, name="iniciar_sesion"),
    path("salir", views.salir, name="salir"),
    #Administrador
    path("admin_inicio", views.admin_inicio, name="admin_inicio"),
    path("admin_frases", views.admin_frases, name="admin_frases"),
    path("admin_pizarron_agregar", views.admin_pizarron_agregar, name="admin_pizarron_agregar"),
    path("admin_pizarron_modificar:<int:pizarron_id>", views.admin_pizarron_modificar, name="admin_pizarron_modificar"),
    path("admin_ejercicio", views.admin_ejercicio, name="admin_ejercicio"),
    path("admin_ejercicio_agregar", views.admin_ejercicio_agregar, name="admin_ejercicio_agregar"),
    path("admin_ejercicio_modificar:<int:ejercicio_id>", views.admin_ejercicio_modificar, name="admin_ejercicio_modificar"),
    path("admin_rutina", views.admin_rutina, name="admin_rutina"),
    path("admin_rutina_agregar", views.admin_rutina_agregar, name="admin_rutina_agregar"),
    path("admin_rutina_modificar:<int:rutina_id>", views.admin_rutina_modificar, name="admin_rutina_modificar"),
    path("admin_rutina_ver:<int:rutina_id>", views.admin_rutina_ver, name="admin_rutina_ver"),
    path("admin_usuarios", views.admin_usuarios, name="admin_usuarios"),
    path("admin_usuarios_agregar", views.admin_usuarios_agregar, name="admin_usuarios_agregar"),
    path("admin_usuarios_CambiarContrasena:<int:usuario_id>", views.admin_usuarios_CambiarContrasena, name="admin_usuarios_CambiarContrasena"),
    path("admin_usuario_premiun:<int:usuario_id>", views.admin_usuario_premiun, name="admin_usuario_premiun"),
    path("admin_usuarios_pesos:<int:usuario_id>", views.admin_usuarios_pesos, name="admin_usuarios_pesos"),
    #Usuario premiun
    path("usuario_inicio", views.usuario_inicio, name="usuario_inicio"),
    path("usuario_rutina:<int:rutina_id>", views.usuario_rutina, name="usuario_rutina"),
    path("usuario_peso", views.usuario_peso, name="usuario_peso"),
    path("usuario_estiramientos", views.usuario_estiramientos, name="usuario_estiramientos"),
    #Usuario gratis
    path("usuario_g", views.usuario_g, name="usuario_g"),
    path("usuario_g_rutinas:<int:rutina_id>", views.usuario_g_rutinas, name="usuario_g_rutinas"),
    path("usuario_g_premiun", views.usuario_g_premiun, name="usuario_g_premiun"),
    #Cambiar contraseña
    path("reset_password/", auth_views.PasswordResetView.as_view(template_name="plataforma/resetear_contrasena.html",html_email_template_name='plataforma/resetear_contrasena_mail.html'), name="reset_password"),
    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(template_name="plataforma/resetear_contrasena_enviado.html"), name="password_reset_done"),
    path("reset_/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(template_name="plataforma/resetear_contrasena_form.html"), name="password_reset_confirm"),
    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(template_name="plataforma/resetear_contrasena_completado.html"), name="password_reset_complete"),
]