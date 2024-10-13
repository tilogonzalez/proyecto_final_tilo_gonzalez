from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Message, Notification
from .forms import MessageForm

def is_admin(user):
    return user.groups.filter(name='Administradora de tienda').exists() or user.is_superuser
class SendMessageView(View):
    def get(self, request):
        form = MessageForm()
        return render(request, 'send_message.html', {
            'form': form,
            'is_admin': is_admin(request.user),
        })

    def post(self, request):
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            
            Notification.objects.create(user=message.recipient, message=message)
            
            return redirect('sent_messages')
        return render(request, 'send_message.html', {
            'form': form,
            'is_admin': is_admin(request.user),
        })

class MessagesView(LoginRequiredMixin, View):
    def get(self, request):
        messages = Message.objects.filter(recipient=request.user).order_by('-sent_date')
        for message in messages:
            if not message.read:
                message.read = True
                message.save()
                
        Notification.objects.filter(user=request.user, read=False).update(read=True)

        return render(request, 'messages.html', {
            'messages': messages,
            'is_admin': is_admin(request.user),
        })

class SentMessagesView(View):
    def get(self, request):
        messages = Message.objects.filter(sender=request.user).order_by('-sent_date')
        return render(request, 'sent_messages.html', {
            'messages': messages,
            'is_admin': is_admin(request.user),
        })