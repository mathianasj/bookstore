from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from library.models import Library
from .models import Author, Book

# Create your tests here.
class AuthorTests(APITestCase):

    def test_create_author(self):
        """
        Ensure we can create a new author object.
        """
        url = '/authors/'
        data = {'first_name': 'First', 'last_name': '1234'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)
        self.assertEqual(response.headers['location'], "/authors/1")
        self.assertEqual(Author.objects.count(), 1)
        self.assertEqual(Author.objects.get().first_name, 'First')

    def test_list_authors(self):
        """
        Ensure we can get the list of authors
        """
        url = '/authors/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_author(self):
        """
        Enusre we can get an author by id
        """
        author = Author()
        author.first_name = "First"
        author.last_name = "Last"
        author.save()
 
        url = "/authors/" + str(author.id)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_author_not_found(self):
        """
        Ensure not found returns 404
        """
        url = "/authors/123456879"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class BookTests(APITestCase):
    def setUp(self):
        self.library = Library()
        self.library.name = "test"
        self.library.address = "address"
        self.library.city = "city"
        self.library.state = "sc"
        self.library.zip = "1234"
        self.library.save()

    def test_create_book(self):
        """
        Ensure we can create a new book object.
        """

        # create temporary author
        author = Author()
        author.first_name = "First"
        author.last_name = "Last"
        author.save()

        url = '/books/'
        data = {'title': 'BookTitle', 'isbn': '1234', 'author': author.id, 'library': self.library.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)
        self.assertEqual(response.headers['location'], "/books/1")
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, 'BookTitle')

    def test_list_books(self):
        """
        Ensure we can get the list of books
        """
        url = '/books/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_book(self):
        """
        Enusre we can get a book by id
        """
        author = Author()
        author.first_name = "First"
        author.last_name = "Last"
        author.save()
        book = Book()
        book.author = author
        book.title = "title"
        book.isbn = "1234"
        book.library = self.library
        book.save()

        url = "/books/" + str(book.id)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "title")
        self.assertEqual(response.data['isbn'], "1234")

    def test_get_book_not_found(self):
        """
        Ensure not found returns 404
        """
        url = "/books/123456879"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)