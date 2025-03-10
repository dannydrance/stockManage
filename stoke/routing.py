from django.urls import path
from stoke.consumers import RFIDConsumer

websocket_urlpatterns = [
    path('ws/rfid/', RFIDConsumer.as_asgi()),
]
