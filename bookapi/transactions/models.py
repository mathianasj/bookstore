from enum import unique
from django.db import models
from books.models import Book
from django.contrib.auth.models import User

from django.utils.translation import gettext_lazy as _

# Create your models here.
class TransactionType(models.TextChoices):
    CHECKOUT = 'CO', _('CHECKOUT')
    CHECKIN = 'CI', _('CHECKIN')

# TODO rethink this design as I would liked to have had immutability of the transaction entries but do not want to have a complex query to get due dates and what is active
class Transaction(models.Model):
    transaction_types = (
        (1, "CHECKOUT"),
        (2, "CHECKIN")
    )

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    transaction_datetime = models.DateTimeField()
    transaction_type = models.CharField(
        max_length=2,
        choices=TransactionType.choices
    )
    due_date = models.DateField(null=True)
    active = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
