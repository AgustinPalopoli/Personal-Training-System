from django.contrib import admin
from .models import User, Ejercicio, Peso,Rutina, Pizarron,Relacion_RyE,Relacion_PyR
# Register your models here.
admin.site.register(User)
admin.site.register(Ejercicio)
admin.site.register(Peso)
admin.site.register(Rutina)
admin.site.register(Pizarron)
admin.site.register(Relacion_RyE)
admin.site.register(Relacion_PyR)