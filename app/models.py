#-*- encoding:utf-8 -*-

from django.db import models
from django.conf import settings

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import random
from django.db.models import fields

from django.db.models.base import Model
from django.db.models.fields import DateTimeField
from django.dispatch import receiver
from django.db.models.signals import post_save


User = get_user_model()


class Proceso(models.Model):
    id = models.AutoField(primary_key = True )
    
    nombre_proceso = models.CharField(max_length = 100)
    correo = models.EmailField(max_length = 100)
    


    
    class Tipo(models.TextChoices):
        PREGUNTAS = '1', "Preguntas"
        VOZ = '2', "VOZ"
        CARTAS = '3', "Cartas"
        VIDEOS = '4',"VIDEOS"
        # (...)

    tipo_quiz = models.CharField(
        max_length=2,
        choices=Tipo.choices,
        default=Tipo.CARTAS
    )

    def __str__(self):
        return self.nombre_proceso
class Pregunta(models.Model):
    
    NUMER_DE_RESPUESTAS_PERMITIDA = 1
    proceso = models.ForeignKey(Proceso, on_delete=models.CASCADE)
    texto = models.TextField(verbose_name='Texto de la Pregunta')
    max_puntaje  = models.DecimalField(verbose_name='Maximo Puntaje',default=3, decimal_places=2,max_digits=6)
    


    def __str__(self):
        return self.texto


class ElegirRespuesta(models.Model):
    
    Maximo_respuesta = 4

    pregunta = models.ForeignKey(Pregunta, related_name='opciones',on_delete=models.CASCADE)
    
    correcta = models.BooleanField(verbose_name='Es esta la respuesta correcta?', default=False, null=False)
    texto = models.TextField(verbose_name='Texto de la respuesta')

    def __str__(self):
        return self.texto


class QuizUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    puntaje_total = models.DecimalField(verbose_name='puntaje total',default=0,decimal_places=2,max_digits=4)

    

    def crear_intentos(self,pregunta):
        intento = PreguntasRespondidas(pregunta=pregunta , quizUser=self)
        intento.save()


    def obtener_nuevas_preguntas(self):
        respondidas = PreguntasRespondidas.objects.filter(quizUser=self).values_list('pregunta__pk',flat=True)
        preguntas_restantes = Pregunta.objects.exclude(pk__in=respondidas)
        if not preguntas_restantes.exists():
            return None
        return random.choice(preguntas_restantes)

        
    def validar_intento(self,pregunta_respondida,respuesta_seleccionada):
        if pregunta_respondida.pregunta_id != respuesta_seleccionada.pregunta_id:
            return
        pregunta_respondida.respuesta_seleccionada = respuesta_seleccionada

        if respuesta_seleccionada.correcta is True:
            pregunta_respondida.correcta = True
            pregunta_respondida.puntaje_obtenido = respuesta_seleccionada.pregunta.max_puntaje
            pregunta_respondida.respuesta = respuesta_seleccionada
        
        else:
            pregunta_respondida.respuesta = respuesta_seleccionada
        pregunta_respondida.save()
        self.actualizar_puntaje()
    def actualizar_puntaje(self):
        puntaje_actualizado = self.intentos.filter(correcta=True).aggregate(models.Sum('puntaje_obtenido'))['puntaje_obtenido__sum']
        self.puntaje_total = puntaje_actualizado
        self.save()
    def preguntas_procesos(self):
        proceso = Proceso.objects.filter(Pregunta=self).values_list('pregunta__pk',flat=True)
        proceso.save()
            



    
    
class PreguntasRespondidas(models.Model):
    
    quizUser = models.ForeignKey(QuizUsuario, on_delete=models.CASCADE, related_name='intentos')
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE)
    respuesta = models.ForeignKey(ElegirRespuesta, on_delete=models.CASCADE, null=True)
    correcta = models.BooleanField(verbose_name='Es esta la pregunta correcta?s', default=False, null=False)
    puntaje_obtenido = models.DecimalField(verbose_name='Puntaje Obtenido', default=0, decimal_places=2,max_digits=6)


class CampanaAsignada(models.Model):
    usuarioasignado = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    procesoasignado = models.ForeignKey(Proceso, null=False, on_delete=models.CASCADE)
    finalizo_campana = models.IntegerField(default=0)
    def __str__(self):
        return "%s %s " % (self.usuarioasignado, self.procesoasignado)
    
class Empresa(models.Model):
    nombre_empresa = models.CharField(max_length = 100)
    status = models.BooleanField(verbose_name='Estado Activo', default=False)
    
    
    def __str__(self):
        return self.nombre_empresa
    








from django.contrib.auth.models import User

class tipo_usuario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa = models.OneToOneField(Empresa,null=True,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='media')
    
    cargo = models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.empresa
    
    

ROLE_CHOICES = (
        (1, 'Admin'),
        (2, 'Evaluador'),
        (3, 'Evaluado'),
        )

class Profile(models.Model):
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)
    
    def __str__(self):
        return str(self.role)


