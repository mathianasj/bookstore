from rest_framework import serializers

from transactions.models import Transaction

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

# used to show the transactions for a book in the user view
class TransactionBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('due_date', 'transaction_type', 'id', 'active', 'transaction_datetime')

# used to show the books that have been or are currently checked out by a user
# i feel like this could be cleaner
# TODO revisit if there is a better way for this, this is not very DRY
class UserBookSerializerList(serializers.ModelSerializer):
    author = AuthorSerializer(source="book.author")
    book_id = serializers.IntegerField(source="book.id")
    transaction_id = serializers.IntegerField(source='id')
    title = serializers.CharField(source="book.title")
    isbn = serializers.CharField(source="book.isbn")

    class Meta:
        model = Transaction
        fields = ('author',
            'book_id',
            'transaction_id',
            'due_date',
            'title',
            'isbn',
            'active')