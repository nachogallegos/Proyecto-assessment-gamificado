from django import forms
from django.db.models import fields

from .models import Pregunta,ElegirRespuesta,PreguntasRespondidas, Proceso,QuizUsuario, CampanaAsignada,Empresa,tipo_usuario,Empresa,Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,get_user_model

User = get_user_model()

class ElegirInLineFormset(forms.BaseInlineFormSet):
    def clean(self):
        super(ElegirInLineFormset, self).clean()

        respuesta_correcta = 0 
        for formulario in self.forms:
            if not formulario.is_valid():
                return
            
            if formulario.cleaned_data and formulario.cleaned_data.get('correcta') is True:
                respuesta_correcta += 1

        try:
            assert respuesta_correcta == Pregunta.NUMER_DE_RESPUESTAS_PERMITIDA
        
        except AssertionError:
            raise forms.ValidationError('SOLO UNA RESPUESTA ES PERMITIDA')


class RegistroFormulario(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
        ]
            
class ProfileRegisterForm(forms.ModelForm):
    class Meta:
        model = tipo_usuario
        fields = ['user','empresa', 'cargo',]
class Roleform(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user','role'] 
        
        
class UsuarioLoginFormulario(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Este Usuario no existe")
            if not user.check_password(password):
                raise  forms.ValidationError("Contraseña Incorrecta")
            if not user.is_active:
                raise forms.ValidationError("Este ususario no esta activo")
        return super(UsuarioLoginFormulario,self).clean(*args, **kwargs)


class preguntaquizform(forms.ModelForm):
    class Meta:
        model = Pregunta
        
        fields = ["proceso",'max_puntaje','texto',]

class respuestaquizform(forms.ModelForm):
    class Meta:
        model = ElegirRespuesta
        
        fields = ['pregunta','correcta','texto',]
    

class tipoproceso(forms.ModelForm):
    class Meta:
        model = Proceso

        fields = ['nombre_proceso','correo','tipo_quiz']
class formcampaña(forms.ModelForm):
    class Meta:
        model = CampanaAsignada
        fields = ['usuarioasignado','procesoasignado']
        
class ListUser(forms.ModelForm):
    class Meta:
        model = User
        fields = [ "username","email","first_name","last_name" ]

class AddEmpresa(forms.ModelForm):
    

    class Meta:
        model = Empresa
        fields = [ "nombre_empresa","status",]

class ResetPasswordForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Ingrese su username',
        'class':'form-control',
        'autocomplete':'off'
    }))