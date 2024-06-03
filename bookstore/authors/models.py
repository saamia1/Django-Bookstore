# Create your models here.
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=255)
    biography = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name