from django.db import models
from django.contrib.auth.models import User


class Messages(models.Model):

    description = models.TextField()
    sender_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender', to_field='id')
    receiver_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver', to_field='id')
    time = models.TimeField(auto_now_add=True,blank=True, null=True)
    seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To: {self.receiver_name} From: {self.sender_name}"

    class Meta:
        ordering = ('timestamp',)


class Friends(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
    friend = models.IntegerField()

    def __str__(self):
        return f"{self.friend}"

