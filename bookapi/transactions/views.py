from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TransactionSerializer, TransactionBookPostSerializer
from .models import Transaction, TransactionType
from books.models import Book
from datetime import datetime, date, timedelta
from rest_framework import generics
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter

# Create your views here.
class TransactionListView(generics.ListAPIView):
    queryset = Transaction.objects.order_by('due_date').all()
    serializer_class = TransactionSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    filterset_fields = ['active', 'book', 'user', 'transaction_type']
    ordering_fields = ['due_date']

class TransactionViews(APIView):
    def get(self, request, id=None):
        try:
            item = Transaction.objects.get(id=id)
            serializer = TransactionSerializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Transaction.DoesNotExist:
            return Response(data=None, status=status.HTTP_404_NOT_FOUND)

class TransactionBookViews(APIView):
    def get(self, request, book_id=None):
        try:
            book = Book.objects.get(id=book_id)
            items = Transaction.objects.filter(book=book)
            serializer = TransactionSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response(data=None, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, book_id):
        serializer = TransactionBookPostSerializer(data=request.data)
        if serializer.is_valid():
            try:
                book = Book.objects.get(id=book_id)

                # add business logic to add due dates and other entries
                today = date.today()
                delta = timedelta(weeks=1)
                serializer.validated_data['book'] = book
                serializer.validated_data['transaction_datetime'] = datetime.now()
                serializer.validated_data['active'] = True

                # get any active transactions for this book
                cotransaction = Transaction.objects.filter(active=True, book=book).first()

                # determine if CO or CI
                if serializer.validated_data['transaction_type'] == TransactionType.CHECKIN:
                    # find active co to mark as not active
                    if cotransaction != None:
                        cotransaction.active = False
                        cotransaction.save()
                    else:
                        return Response(data={"msg":"check out not found"}, status=status.HTTP_404_NOT_FOUND)
                else:
                    if cotransaction != None:
                        return Response(data=None, status=status.HTTP_400_BAD_REQUEST)

                    # add the due date since this is a check out
                    serializer.validated_data['due_date'] = today + delta

                # save the transaction
                serializer.save()
                return Response(status=status.HTTP_303_SEE_OTHER, headers={"location": "/transactions/" + str(serializer.data['id'])})
            except Book.DoesNotExist:
                return Response(data=None, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)