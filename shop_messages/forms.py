from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'content']
        labels = {
            'recipient': 'Destinatario',
            'content': 'Contenido del Mensaje',
        }