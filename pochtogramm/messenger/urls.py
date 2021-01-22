from django.urls import path

from .views import hello, chat_box, send, flooders, search

urlpatterns = [
    path('', hello, name='index'),
    path('chat_box/', chat_box, name='chat_box'),
    path('search/', search, name='search'),
    path('flooders/', flooders, name='flooders'),
    path('send/', send, name='send'),
]
