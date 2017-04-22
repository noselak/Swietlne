from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(null=True, blank=True, max_length=70)
    address = models.CharField(null=True, blank=True, max_length=70)
    phone = models.CharField(null=True, blank=True, max_length=15)
    
    class Meta:
        verbose_name = 'Profil użytkownika'
        verbose_name_plural = 'Profile użytkowników'
    
    def __str__(self):
        return self.user.username