from django.contrib.auth.models import AbstractUser
from django.db import models

class Ejercicio(models.Model):
    tipo = models.CharField(max_length=128)
    grupo_muscular = models.CharField(max_length=128,blank=True,null=True)
    nombre_ej = models.CharField(max_length=128,blank=True,null=True)
    series =models.CharField(max_length=128,blank=True,null=True)
    repeticiones = models.CharField(max_length=128,blank=True,null=True)
    descanso = models.DurationField(blank=True,null=True)
    peso_con_sin = models.CharField(max_length=128)
    imagen = models.ImageField()

class Peso(models.Model):
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE, related_name = "ejercicio",blank=True,null=True)
    fecha = models.DateTimeField(blank=True,null=True)
    cantidad_peso = models.CharField(max_length=64)

class User(AbstractUser):
    telefono = models.CharField(max_length=128,blank=True,null=True)
    sexo = models.CharField(max_length=128)
    pesos = models.ManyToManyField(Peso, related_name = "rutinas_semana", default = None,blank=True)
    USER_TYPE_CHOICES = (
      (1, 'admin'),
      (2, 'user'),
      (3, 'premiun'),
    )
    rol = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default = 1)
    class Meta:
        permissions = (("ADMIN", "is_admin"),("USER", "is_user"),("PREMIUN","is_premiun"))


class Rutina(models.Model):
    nombre_rutina = models.CharField(max_length=128)
    tipo_usuario = models.CharField(max_length=128)
    tipo_sexo = models.CharField(max_length=128, default = None,null=True)

class Relacion_RyE(models.Model):
    rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE,related_name = "rutina", default = None)
    ej = models.ForeignKey(Ejercicio, on_delete=models.CASCADE, related_name = "ej", default = None)
    orden = models.CharField(max_length=128,blank=True,null=True)

class Pizarron(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "usuario", default = None)
    mensaje = models.CharField(max_length=128,blank=True,null=True)

class Relacion_PyR(models.Model):
    pizarron_rutina = models.ForeignKey(Rutina, on_delete=models.CASCADE,related_name = "pizarron_rutina", default = None)
    pizarron_id = models.ForeignKey(Pizarron, on_delete=models.CASCADE, related_name = "pizarron_id", default = None)
    orden = models.CharField(max_length=128,blank=True,null=True)