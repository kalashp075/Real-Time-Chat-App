# Basic Django imports
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import ChatRoom, Message
from .forms import CleanUserCreationForm, CleanLoginForm
from django.contrib.auth.models import User
from .models import ChatRoom, Message, OnlineUser
from .forms import CleanUserCreationForm

def register_view(request):
    if request.method == 'POST':
        form = CleanUserCreationForm(request.POST)  # Form filled with user's submitted data
        if form.is_valid():
            user = form.save()
            return redirect('login')
    else:
        form = CleanUserCreationForm()  # Empty form for display/GET request
            
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CleanLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('lobby')
    else:
        form = CleanLoginForm()
    
    return render(request, 'registration/login.html', {'form': form})
            
@login_required
def lobby_view(request):
    # Update current user's online status
    OnlineUser.update_last_seen(request.user)
    
    # Get all users and their online status
    users = User.objects.all()
    online_user_ids = set(OnlineUser.get_online_users().values_list('user_id', flat=True))
    
    # Add online status to users
    for user in users:
        user.is_online = user.id in online_user_ids
    
    return render(request, 'lobby.html', {'users': users})

@login_required
def start_chat(request, user_id):
    # Get the other user
    other_user = User.objects.get(id=user_id)
    current_user = request.user
    
    # Can't chat with yourself!
    if other_user == current_user:
        return redirect('lobby')
    
    # Find existing chat room (check both user combinations)
    chatroom = ChatRoom.objects.filter(
        user1=current_user, user2=other_user
    ).first() or ChatRoom.objects.filter(
        user1=other_user, user2=current_user
    ).first()
    
    # Create new room if none exists
    if not chatroom:
        chatroom = ChatRoom.objects.create(
            user1=current_user,
            user2=other_user
        )
    
    # Redirect to chat interface
    return redirect('chat_room', room_id=chatroom.id)

@login_required
def chat_room(request, room_id):
    # Update current user's online status
    OnlineUser.update_last_seen(request.user)
    
    # Get the chat room
    chatroom = ChatRoom.objects.get(id=room_id)
    
    # Make sure user is part of this chat
    if request.user not in [chatroom.user1, chatroom.user2]:
        return redirect('lobby')
    
    # Get previous messages
    messages = Message.objects.filter(chatroom=chatroom).order_by('timestamp')
    
    # Get the other user's name
    other_user = chatroom.user2 if chatroom.user1 == request.user else chatroom.user1
    
    # Get all users for sidebar
    all_users = User.objects.all()
    
    return render(request, 'chat_room.html', {
        'room_id': room_id,
        'messages': messages,
        'other_user': other_user,
        'all_users': all_users,
    })
