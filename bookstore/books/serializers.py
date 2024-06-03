from rest_framework import serializers
from .models import Book
from authors.models import Author
from categories.models import Category

class BookSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'isbn', 'category']

