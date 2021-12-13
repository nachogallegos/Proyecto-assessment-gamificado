from django.contrib import admin
from .models import *

from .forms import ElegirInLineFormset

class ElegirRespuestaInline(admin.TabularInline):
    model = ElegirRespuesta
    max_num = ElegirRespuesta.Maximo_respuesta
    min_num = ElegirRespuesta.Maximo_respuesta
    formset = ElegirInLineFormset
    


class PreguntaAdmin(admin.ModelAdmin):
    model = Pregunta
    inlines = (ElegirRespuestaInline, )
    list_display = ['texto',]
    search_fields = ['texto','preguntas__texto']

class PreguntasRespondidasAdmin(admin.ModelAdmin):
    list_display=['pregunta','respuesta','correcta','puntaje objtenido']


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['user']
    list_display = ('id','role', 'user')


# Register your models here.
admin.site.register(Proceso)
admin.site.register(Pregunta, PreguntaAdmin)
admin.site.register(ElegirRespuesta)
admin.site.register(QuizUsuario)
admin.site.register(PreguntasRespondidas)
admin.site.register(CampanaAsignada)
admin.site.register(Empresa)
admin.site.register(tipo_usuario)
admin.site.register(Profile,ProfileAdmin)


