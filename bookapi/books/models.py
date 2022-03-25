from django.db import models

from library.models import Library

# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=200, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)
    # TODO would like to have duedate placed here in response to event driven architecture instead of having to do a join query against the transactions
    # this will be part of breaking out these into separate services so they are not coupled to each other