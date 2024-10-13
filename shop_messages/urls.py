from django.urls import path
from .views import SendMessageView, MessagesView, SentMessagesView

urlpatterns = [
    path('send/', SendMessageView.as_view(), name='send_message'),
    path('messages/', MessagesView.as_view(), name='messages'),
    path('sent/', SentMessagesView.as_view(), name='sent_messages'),
]