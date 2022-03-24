from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Library

# Create your tests here.
class LibraryTests(APITestCase):
    def test_create_library(self):
        """
        Ensure we can create a new author object.
        """
        url = '/library/'
        data = {'name': 'Hilton Head Library', 'address': "123 Beach Street", 'city':'Hilton Head Island', 'state':'SC', 'zip':'29926'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_303_SEE_OTHER)
        self.assertEqual(response.headers['location'], "/library/1")
        self.assertEqual(Library.objects.count(), 1)
        self.assertEqual(Library.objects.get().name, 'Hilton Head Library')
        self.assertEqual(Library.objects.get().address, '123 Beach Street')
        self.assertEqual(Library.objects.get().city, 'Hilton Head Island')
        self.assertEqual(Library.objects.get().state, 'SC')
        self.assertEqual(Library.objects.get().zip, '29926')

    def test_list_libraries(self):
        """
        Ensure we can get the list of libraries
        """
        url = '/library/'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_library(self):
        """
        Enusre we can get an library by id
        """
        library = Library()
        library.name = "not real"
        library.address = "456 Street"
        library.city = "Austin"
        library.state = "TX"
        library.zip = "12345"
        library.save()
 
        url = "/library/" + str(library.id)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], library.name)
        self.assertEqual(response.data['address'], library.address)
        self.assertEqual(response.data['city'], library.city)
        self.assertEqual(response.data['state'], library.state)
        self.assertEqual(response.data['zip'], library.zip)

    def test_get_library_not_found(self):
        """
        Ensure not found returns 404
        """
        url = "/library/123456879"
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
