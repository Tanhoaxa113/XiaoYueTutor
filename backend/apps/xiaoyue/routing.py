from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<user_id>[^/]+)/$', consumers.ChineseTutorConsumer.as_asgi()),

    re_path(r'ws/chat/$', consumers.ChineseTutorConsumer.as_asgi()),
]

