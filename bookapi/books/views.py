from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from transactions.models import Transaction

from transactions.models import TransactionType
from .serializers import AuthorSerializer, BookSerializer, BookSerializerList, UserBookSerializerList
from .models import Author, Book
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework import generics

# Create your views here.
## Doing this one here to limit the amount of eventing to occur to keep the two in sync make it more of a macro api
class AuthorViews(APIView):
    def get(self, request, id=None):
        if id:
            try:
                item = Author.objects.get(id=id)
                serializer = AuthorSerializer(item)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Author.DoesNotExist:
                return Response(data=None, status=status.HTTP_404_NOT_FOUND)

        items = Author.objects.all()
        serializer = AuthorSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_303_SEE_OTHER, headers={"location": "/authors/" + str(serializer.data['id'])})
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class BookViews(APIView):
    def get(self, request, id=None):
        if id:
            try:
                item = Book.objects.get(id=id)
                serializer = BookSerializerList(item)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Book.DoesNotExist:
                return Response(data=None, status=status.HTTP_404_NOT_FOUND)

        items = Book.objects.all()
        serializer = BookSerializerList(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_303_SEE_OTHER, headers={"location": "/books/" + str(serializer.data['id'])})
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class UserBookViews(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = UserBookSerializerList
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    ordering_fields = ['due_date', 'author__first_name', 'author__last_name']
    filterset_fields = ['book__title', 'book__author__first_name', 'book__author__last_name', 'book__id', 'active']
    
    def get_queryset(self):
        return Transaction.objects.filter(user__id=self.kwargs['user_id'], transaction_type=TransactionType.CHECKOUT).order_by("due_date")