# Chat WebSocket Consumer
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the room ID from URL (like: /ws/chat/123/)
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        
        # Create a unique group name for this chat room
        self.room_group_name = f'chat_{self.room_id}'
        
        # Join the room group (subscribe to broadcasts)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        # Accept the WebSocket connection
        await self.accept()
    
    async def disconnect(self, close_code):
        # Leave the room group (unsubscribe from broadcasts)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        # Parse the incoming message
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']
        username = text_data_json['username']
        
        # Save message to database
        await self.save_message(username, message_content)
        
        # Broadcast message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_content,
                'username': username,
            }
        )
    
    # Handle message broadcasting
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
        }))
    
    # Database operations (sync to async)
    @database_sync_to_async
    def save_message(self, username, message):
        from django.contrib.auth.models import User
        from .models import ChatRoom, Message
        
        user = User.objects.get(username=username)
        chatroom = ChatRoom.objects.get(id=self.room_id)
        Message.objects.create(
            chatroom=chatroom,
            sender=user,
            content=message
        )
