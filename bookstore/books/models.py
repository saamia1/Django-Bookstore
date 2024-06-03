from django.db import models
from authors.models import Author
from categories.models import Category

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey('authors.Author', on_delete=models.CASCADE)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    category = models.ForeignKey('categories.Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.title