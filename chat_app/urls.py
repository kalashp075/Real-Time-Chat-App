
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.lobby_view, name='lobby'),
    path('chat/<int:user_id>/', views.start_chat, name='start_chat'),
    path('room/<int:room_id>/', views.chat_room, name='chat_room'),
]
