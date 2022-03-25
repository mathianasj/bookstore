from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from library.models import Library
from .models import Transaction, TransactionType
from books.models import Author, Book
from datetime import date, timedelta, datetime
from django.contrib.auth.models import User

# This is not an inclusive list of all tests, just a demonstration of unique features
class TransactionTest(APITestCase):
    def setUp(self):
        author = Author()
        author.first_name = "First"
        author.last_name = "Last"
        author.save()

        library = Library()
        library.name = "test"
        library.address = "address"
        library.city = "city"
        library.state = "sc"
        library.zip = "1234"
        library.save()

        self.book = Book()
        self.book.title = "Book Title"
        self.book.isbn = "12345"
        self.book.author = author
        self.book.library = library
        self.book.save()

        self.user = User()
        self.user.set_password("abcdef")
        self.user.username = "testuser"
        self.user.save()

    def test_checkout(self):
        """
        Ensure we can checkout a book.
        """
        url = '/books/' + str(self.book.id) + '/transaction'
        data = {'transaction_type': 'CO', 'user': self.user.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)
        self.assertEqual(response.headers['location'], "/transactions/1")
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Transaction.objects.get().transaction_type, 'CO')
        self.assertEqual(Transaction.objects.get().book.id, self.book.id)
        
        # calculate 2 weeks from now
        today = date.today()
        delta = timedelta(weeks=1)
        duedate = today + delta
        self.assertEqual(Transaction.objects.get().due_date, duedate)

    def test_ceckin_without_checkout_fails(self):
        """
        Ensure we cannot checkin without checkout
        """
        url = '/books/' + str(self.book.id) + '/transaction'
        data = {'transaction_type': 'CI', 'user': self.user.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['msg'], "check out not found")

    def test_list_transactions(self):
        """
        Ensure we can get the list of books
        """
        url = '/transactions/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Transaction.objects.count())

    def test_get_transaction(self):
        """
        Enusre we can get a transaction by id
        """
        transaction = Transaction()
        transaction.transaction_datetime = datetime.now()
        transaction.transaction_type = TransactionType.CHECKOUT
        transaction.due_date = date.today()
        transaction.active = True
        transaction.book = self.book
        transaction.user = self.user
        transaction.save()

        url = "/transactions/" + str(transaction.id)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['book'], self.book.id)

    def test_transaction_not_found(self):
        """
        Ensure not found returns 404
        """
        url = "/transactions/123456879"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)