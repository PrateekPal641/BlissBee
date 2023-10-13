from django.db import models
from django.contrib.auth.models import User
from django.db import models
import json
import os
import jsonpickle

def generate_image_filename(instance, filename):
    # Get the file extension
    file_extension = os.path.splitext(filename)[1]
    
    # Generate a unique filename using title and created_at fields
    unique_filename = f"{instance.title}_{instance.created_at.strftime('%Y%m%d%H%M%S')}{file_extension}"
    
    # Return the path to the image
    return os.path.join('scenario_images', unique_filename)


class Feeling(models.Model):
    name = models.CharField(max_length=50, unique=True)

class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    
    RELATIONSHIP_CHOICES = (
        ('Single', 'Single'),
        ('In a relationship', 'In a relationship'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    relationship_status = models.CharField(max_length=20, choices=RELATIONSHIP_CHOICES, blank=True, null=True)
    
    moving_summary_buffer = models.TextField(default="",blank=True, null=True)
    chat_memory_messages = models.TextField(default=jsonpickle.dumps([]),blank=True, null=True)  # Default to an empty list JSON string
    illness = models.TextField(default="",blank=True, null=True)

    def set_message_list(self, chat_memory_messages):
        return jsonpickle.dumps(chat_memory_messages)

    def get_message_list(self):
        return jsonpickle.loads(self.chat_memory_messages)
    
    def __str__(self):
        return self.user.username
    
    
class Material(models.Model):
    materialId = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    link = models.URLField(max_length=300)
    feelings = models.ManyToManyField(Feeling)

    def __str__(self):
        return self.title

class Activity(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()  # Add a date field
    duration = models.DurationField(null=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class ScenarioFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(default="")
    scenario = models.TextField()
    response = models.TextField()
    feedback = models.TextField()
    rating = models.IntegerField(default=1)
    image = models.ImageField(upload_to=generate_image_filename, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user.username}, Date: {self.created_at}" 

class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    objective = models.TextField()
    timeframe = models.TextField()
    strategies = models.TextField(default=jsonpickle.dumps([]),blank=True, null=True)  # Store strategies as a list, serialized as JSON
    quote = models.TextField()

    def __str__(self):
        return self.title