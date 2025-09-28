# WebSocket URL routing
from django.urls import re_path
from . import consumers

# This file defines which WebSocket URLs are handled by which consumers
# Think of it like urls.py but for WebSocket connections
websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
