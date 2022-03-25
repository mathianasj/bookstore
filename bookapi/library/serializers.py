from rest_framework import serializers
from books.models import Book

from transactions.models import Transaction

from .models import Library

class LibrarySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)
    address = serializers.CharField(max_length=200)
    city = serializers.CharField(max_length=200)
    state = serializers.CharField(max_length=2)
    zip = serializers.CharField(max_length=5)

    class Meta:
        model = Library
        fields = ('__all__')

class CheckOutRelatedField(serializers.RelatedField):
    def to_representation(self, instance):
        return instance.active

# TODO this is not exactly correct will need to research more the correct way to get the joins to work
class LibraryBookSerializer(serializers.ModelSerializer):
    transaction_set = CheckOutRelatedField(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ('id', 'title', 'isbn', 'author', 'transaction_set')