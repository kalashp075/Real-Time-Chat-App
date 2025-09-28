from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.utils import timezone

class ChatRoom(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatrooms_as_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatrooms_as_user2')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Chat between {self.user1.username} and {self.user2.username}"
    
    def get_other_user(self, user):
        """Given one user, return the other user in this chat"""
        return self.user2 if user == self.user1 else self.user1
    
class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"
    
    class Meta:
        ordering = ['timestamp']  # Show messages in chronological order

class OnlineUser(models.Model):
    """Track which users are currently online"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_seen = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} - {self.last_seen}"
    
    @classmethod
    def update_last_seen(cls, user):
        """Update user's last seen timestamp"""
        obj, created = cls.objects.get_or_create(user=user)
        obj.last_seen = timezone.now()
        obj.save()
    
    @classmethod
    def get_online_users(cls):
        """Get users who were active in the last 5 minutes"""
        threshold = timezone.now() - timezone.timedelta(minutes=5)
        return cls.objects.filter(last_seen__gte=threshold).select_related('user')
