from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/meeting/<int:meeting_id>/', consumers.VideoCallConsumer.as_asgi()),
]
