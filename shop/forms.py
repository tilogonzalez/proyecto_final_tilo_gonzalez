from django import forms
from .models import Product, Service, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'brand', 'description', 'price', 'image', 'stock']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['image'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['style'] = 'margin-top: 30px; font-size: 14px;'

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description', 'price', 'duration', 'image']
        
class SearchForm(forms.Form):
    query = forms.CharField(
        label='Buscar Producto',
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Buscar producto',
        })
    )

class CustomUserCreationForm(UserCreationForm):
    address = forms.CharField(max_length=255, required=False, label='Dirección')
    phone_number = forms.CharField(max_length=20, required=False, label='Número de teléfono')

    class Meta:
        model = User
        fields = (
            'username', 
            'email', 
            'password1', 
            'password2', 
            'address', 
            'phone_number'
        )
        labels = {
            'username': 'Nombre de usuario',
            'email': 'Correo electrónico',
            'password1': 'Contraseña',
            'password2': 'Repetir contraseña',
        }
        help_texts = {
            'username': 'Requerido. Únicamente letras, números y @/./+/-/_',
            'email': 'Introduce una dirección de correo electrónico válida.',
            'password1': (
                'Su contraseña no puede asemejarse tanto a su otra información personal.\n'
                'Su contraseña debe contener al menos 8 caracteres.\n'
                'Su contraseña no puede ser una clave utilizada comúnmente.\n'
                'Su contraseña no puede ser completamente numérica.'
            ),
            'password2': 'Repite la contraseña anterior.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['title'] = field.help_text

class ProfileEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Profile
        fields = ['email', 'address', 'phone_number', 'profile_picture']
        labels = {
            'email': 'Correo electrónico',
            'address': 'Dirección',
            'phone_number': 'Número de teléfono',
            'profile_picture': 'Imagen de perfil',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email

        self.fields['profile_picture'].widget.attrs['class'] = 'form-control'
        self.fields['profile_picture'].widget.attrs['style'] = 'margin-top: 30px; font-size: 14px;'

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Nombre', required=False)
    email = forms.EmailField(label='Correo electrónico')
    message = forms.CharField(widget=forms.Textarea, label='Mensaje')
    
class ClientEditForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Profile
        fields = ['email', 'address', 'phone_number', 'profile_picture']
        labels = {
            'email': 'Correo electrónico',
            'address': 'Dirección',
            'phone_number': 'Número de teléfono',
            'profile_picture': 'Imagen de perfil',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email