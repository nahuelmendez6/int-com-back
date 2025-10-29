from django.db import models
from django.conf import settings

class Conversation(models.Model):

    id_conversation = models.AutoField(primary_key=True)
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'n_conversation'
        ordering = ['-created_at']
        managed = False

    def __str__(self):
        participants = ", ".join([u.email for u in self.partipants.all()])
        return f"Conversación {self.id_conversation} ({participants})"
    
    def get_other_participant(self, user):
        return self.partipants.exclude(id_user=user.id_user).first()
    

class Message(models.Model):

    id_message = models.AutoField(primary_key=True)
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        db_table = 'n_message'
        ordering = ['created_at']
        managed = False

    def __str__(self):
        return f"{self.sender.email}: {self.content[:20]}"