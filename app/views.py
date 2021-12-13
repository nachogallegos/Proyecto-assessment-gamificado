#-*- encoding:utf-8 -*-
from django.contrib.auth.models import User
from django.contrib import admin
from django.http.response import Http404
from django.shortcuts import render,redirect,get_object_or_404
from .forms import ListUser, RegistroFormulario,UsuarioLoginFormulario, preguntaquizform,respuestaquizform,tipoproceso,formcampaña,ResetPasswordForm,AddEmpresa,Roleform,ProfileRegisterForm

from django.contrib.auth import authenticate, login, logout
from .models import  Proceso, QuizUsuario,Pregunta,PreguntasRespondidas, CampanaAsignada, Profile,Empresa,tipo_usuario
from django.http import HttpResponseNotFound
from django.core.exceptions import ObjectDoesNotExist
# from django.core.cache import cache
from django.shortcuts import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import HttpResponseRedirect
from django.contrib import messages

# Create your views here.

@login_required
def HomeUsuario(request):
    
    context = {}
    if request.session:
        try:
            profile = Profile.objects.get(user=request.session['_auth_user_id'])
            request.session['profile'] = profile.role
            
            if profile.role == 1:
                context['admin'] = True
            if profile.role == 2:
                context['evaluador'] = True
            if profile.role == 3:
                context['evaluado'] = True

        except Profile.DoesNotExist:
            raise Http404
    
    return render(request,'Usuario/homeusuario.html', context)
            
def home(request):
    return render(request,'Usuario/login.html')


@login_required
def perfil(request):
    return render(request,'perfil.html')

@login_required
def crearquiz(request):

    return render(request,'crearquiz.html')
@login_required
def tablero(request):
    total_usuarios_quiz = QuizUsuario.objects.order_by('-puntaje_total')[:10]
    contador = total_usuarios_quiz.count()

    context = {
        'usuario_quiz':total_usuarios_quiz,
        'contar_user':contador
    }
    return render(request,'Play/tablero.html',context)

def jugarvideo(request):
    return render(request,'Play/jugarvideo.html')
@login_required
def evaluados(request):
    total_usuarios_quiz = QuizUsuario.objects.all()
    datos_user = User.objects.all()

    context = {
        'usuario_quiz':total_usuarios_quiz,
        'datos_user':datos_user
    }
    return render(request,'Play/tablaevaluados.html',context)
def tablaempresas(request):
    
    datos_empresas = Empresa.objects.all()
    datos_user = tipo_usuario.objects.all()

    context = {
        
        'datos_empresas':datos_empresas,
        'datos_user':datos_user
    }
    return render(request,'Play/tablaempresas.html',context)

def loginView(request):
    titulo='login'
    form = UsuarioLoginFormulario(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        usuario = authenticate(username=username, password=password)
        login(request, usuario)
        return redirect ('HomeUsuario')
    context = {
        'form':form,
        'titulo':titulo
    }
    return render (request, 'Usuario/login.html',context)

@login_required
def logout_vista(request):
    logout(request)
    return redirect('/')

@login_required
def jugar(request):
    
    QuizUser, created = QuizUsuario.objects.get_or_create(usuario=request.user)


    if request.method == 'POST': 
        
        pregunta_pk = request.POST.get('pregunta_pk')
        
        pregunta_respondida = QuizUser.intentos.select_related('pregunta').get(pregunta__pk=pregunta_pk)
        respuesta_pk = request.POST.get('respuesta_pk')
        
        try:
           opcion_seleccionada = pregunta_respondida.pregunta.opciones.get(pk=respuesta_pk)
        except ObjectDoesNotExist:
                raise Http404
        QuizUser.validar_intento(pregunta_respondida,opcion_seleccionada)

        return redirect('resultado', pregunta_respondida.pk)
    
    else:
        pregunta = QuizUser.obtener_nuevas_preguntas()
        if pregunta is not None:
            QuizUser.crear_intentos(pregunta)
        context = {
            'pregunta':pregunta,
            

        }
    
    return render(request, 'Play/jugar.html' , context)





@login_required
def resultado_pregunta(request,pregunta_respondida_pk):
    respondida=get_object_or_404(PreguntasRespondidas,pk=pregunta_respondida_pk)
    context = {
        'respondida':respondida
    }
    return render(request,'Play/resultados.html',context)

    

@login_required
def registro(request):
    
        data = {
            'form':RegistroFormulario()
        }
        # create a form instance and populate it with data from the request:
        if request.method == 'POST':
            formulario=RegistroFormulario(data=request.POST)
            if formulario.is_valid():
                formulario.save()
                user = authenticate(username=formulario.cleaned_data["username"],password=formulario.cleaned_data["password1"])
                login(request,user)
                messages.success(request , "Se ha registrado el usuario")
        # check whether it's valid:
            return HttpResponseRedirect('registro')
            data["form"] = formulario

            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            

    # if a GET (or any other method) we'll create a blank form
    

        return render(request, 'Usuario/registro.html', data)
def roles(request):
       
    data = {
        'form':Roleform(data=request.POST),
        
    }
        
    
    if request.method=='POST':
        formulario=Roleform(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('roles')

        else:
            data["form"] = formulario




    

    return render(request, 'Usuario/registroroles.html', data)
def empresauser(request):
       
    data = {
        'form':ProfileRegisterForm(data=request.POST),
        
    }
        
    
    if request.method=='POST':
        formulario=ProfileRegisterForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('registroempresa')

        else:
            data["form"] = formulario




    

    return render(request, 'Usuario/registroempresa.html', data)
def empresa(request):
       
    data = {
        'form':AddEmpresa(data=request.POST),
        
    }
        
    
    if request.method=='POST':
        formulario=AddEmpresa(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('empresa')

        else:
            data["form"] = formulario




    

    return render(request, 'Usuario/registroempresa.html', data)
    
@login_required
def agregar_quiz(request):

    data = {
        'form':preguntaquizform(),
        
    }
    if request.method=='POST':
        formulario=preguntaquizform(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            data['mensaje']= "guardado correctamente"

        else:
            data["form"] = formulario




    return render(request,'agregarquiz.html',data)
@login_required
def agregar_respuesta(request):
    
    data = {
        'form':respuestaquizform(),
        
    }
    if request.method=='POST':
        formulario=respuestaquizform(data=request.POST, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect('agregarrespuestas')

        else:
            data["form"] = formulario




    return render(request,'agregarrespuestas.html',data)

@login_required



@login_required
def tipo_proceso(request):
    
    
    data = {
        'form':tipoproceso(data=request.POST),
        
    }
        
    
    if request.method=='POST':
        formulario=tipoproceso(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('agregarquiz')

        else:
            data["form"] = formulario




    return render(request,'crearquiz.html',data)
    
@login_required  
def procesosasignados(request):
    
    
    data = {
        'form':formcampaña(data=request.POST),
        
        
    }
        
    
    if request.method=='POST':
        formulario=formcampaña(data=request.POST)
        if formulario.is_valid():

            formulario.save()
            return redirect('procesosasignados')

        else:
            data["form"] = formulario




    return render(request,'Procesosasignados.html',data)
    
   

@login_required
def tablaprocesos(request):
    total_procesos = CampanaAsignada.objects.all()
    campana_proceso = Proceso.objects.all()
    

    context = {
        'total_procesos':total_procesos,
        'campaña_proceso':campana_proceso
        
        
    }
    return render(request,'tablaprocesos.html',context)

@login_required
def mostrar_procesos_incompletos(request):
    from django.contrib.auth.models import User
    from django.db.models import Q
    id_usuario = User.objects.filter(username=str(request.user))
    id_usuario = id_usuario[0].id
    campanas_incompletas = CampanaAsignada.objects.filter(Q(usuarioasignado_id=id_usuario) & Q(finalizo_campana=0))
    nombre_procesos_incompletos = []
    for proceso in campanas_incompletas:
        nombre_procesos_incompletos.append(str(proceso.procesoasignado))
    context = {
        'total_procesos':len(nombre_procesos_incompletos) if len(nombre_procesos_incompletos) > 0 else 0,
        'campaña_proceso':nombre_procesos_incompletos
    }
    return render(request,'tablaprocesos.html',context)
    
def mostrar_preguntas_proceso(request,proceso):
    
    try:
        id_proceso = Proceso.objects.filter(nombreproceso=proceso)
        id_proceso = id_proceso[0].id
        preguntas = Pregunta.objects.filter(proceso_id=id_proceso)
        #se puede especificar el campo preguntas.cualquier camnpo
        #retornar con un template
        preguntas = [i.texto for i in preguntas]
        return HttpResponse(str(preguntas))

    except Exception as e:
        return HttpResponse("Ocurrio el siguiente error "+str(e))



"""
campañas incompletas va a devolver las campañas que estan incompletas por ese usario
Esas campañas(procesos) van hacer un enlace porque se va a rellenar en un contexto en un tem,pleate
Al hacer clic en un proceso se van a obtener todos las preguntas de ese proceso
"""
@login_required
def modificarUser(request,id):
    detalle = User.objects.get(id=id)
    data={
        'form':ListUser(instance = detalle)
    }

    if request.method =='POST':
        formulario =  ListUser (data=request.POST,instance=detalle)
        if formulario.is_valid():
            formulario.save()
            data['mensaje'] = "Modificado Correctamente"
            data['form'] = formulario
            
    return render(request,'Usuario/modificarusuario.html',data)

@login_required
def modificarempresa(request,id):
    detalle = Empresa.objects.get(id=id)
    data={
        'form':AddEmpresa(instance = detalle)
    }

    if request.method =='POST':
        formulario =  AddEmpresa (data=request.POST,instance=detalle)
        if formulario.is_valid():
            formulario.save()
            data['mensaje'] = "Modificado Correctamente"
            data['form'] = formulario
            
    return render(request,'Usuario/modificarrempresa.html',data)

@login_required
def modificartipouser(request,id):
    detalle = tipo_usuario.objects.get(id=id)
    data={
        'form':ProfileRegisterForm(instance = detalle)
    }

    if request.method =='POST':
        formulario =  ProfileRegisterForm (data=request.POST,instance=detalle)
        if formulario.is_valid():
            formulario.save()
            data['mensaje'] = "Modificado Correctamente"
            data['form'] = formulario
            
    return render(request,'Usuario/modificartipouser.html',data)

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import (
    url_has_allowed_host_and_scheme, urlsafe_base64_decode,
)
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title,
            **(self.extra_context or {})
        })
        return context

class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = 'regitstration/password_reset_done.html'
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'regitstration/password_reset_form.html'
    title = _('Password reset')
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)


INTERNAL_RESET_SESSION_TOKEN = '_password_reset_token'


class PasswordResetDoneView(PasswordContextMixin, TemplateView):
    template_name = 'regitstration/password_reset_done.html'
    title = _('Password reset sent')


class PasswordResetConfirmView(PasswordContextMixin, FormView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    reset_url_token = 'set-password'
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'regitstration/password_reset_confirm.html'
    title = _('Enter new password')
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        if 'uidb64' not in kwargs or 'token' not in kwargs:
            raise ImproperlyConfigured(
                "The URL path must contain 'uidb64' and 'token' parameters."
            )

        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if token == self.reset_url_token:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(token, self.reset_url_token)
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist, ValidationError):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context['validlink'] = True
        else:
            context.update({
                'form': None,
                'title': _('Password reset unsuccessful'),
                'validlink': False,
            })
        return context


class PasswordResetCompleteView(PasswordContextMixin, TemplateView):
    template_name = 'regitstration/password_reset_confirm.html'
    title = _('Password reset complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_url'] = resolve_url(settings.LOGIN_URL)
        return context


class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'regitstration/password_reset_form.html'
    title = _('Password change')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


class PasswordChangeDoneView(PasswordContextMixin, TemplateView):
    template_name = 'regitstration/password_reset_done.html'
    title = _('Password change successful')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

from .models import Video
from .forms import VideoForm

def showvideo(request):
   
    lastvideo= Video.objects.last()

    videofile = lastvideo.videofile if lastvideo else None


    form= VideoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()

    
    context= {'videofile': videofile,
              'form': form
              }
    
      
    return render(request, 'Usuario/videos.html', context,)


