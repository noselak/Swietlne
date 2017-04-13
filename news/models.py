from django.db import models


class Join(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
        
class Faq(models.Model):
    question = models.TextField()
    answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["timestamp"]
    
    def __str__(self):
        return self.question
    
    