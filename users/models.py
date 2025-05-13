from django.db import models
from django.contrib.auth.models import User
from typing import Any

# Create your models here.

class Profile(models.Model):
    """
    User profile model to extend the built-in Django User model.
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    
    # Add additional fields if needed
    
    def __str__(self) -> str:
        return f"{self.user.username} Profile"
