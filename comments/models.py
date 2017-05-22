from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Comment(models.Model):
    comment_username = models.CharField(max_length=40)
    comment_body = models.TextField()
    comment_parent = models.ForeignKey('self', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        ordering = ['-timestamp']
        
    def __str__(self):
        return self.comment_username + ": " + self.comment_body
    
    @property    
    def children(self):
        return Comment.objects.filter(comment_parent=self)
        
    @property
    def is_parent(self):
        if self.comment_parent is None:
            return True
        return False
