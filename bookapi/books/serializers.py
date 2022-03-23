from rest_framework import serializers
from .models import Author, Book

class AuthorSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)

    class Meta:
        model = Author
        fields = ('__all__')

class BookSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=200)
    isbn = serializers.CharField(max_length=200)
    author = serializers.IntegerField

    class Meta:
        model = Book
        fields = ('__all__')

class BookSerializerList(serializers.ModelSerializer):
    author = AuthorSerializer(many=False, read_only=True)

    class Meta:
        model = Book
        fields = ('__all__')