from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from transactions.models import Transaction

from transactions.models import TransactionType
from .serializers import LibrarySerializer
from .models import Library
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework import generics

# Create your views here.
## Doing this one here to limit the amount of eventing to occur to keep the two in sync make it more of a macro api
class LibraryViews(APIView):
    def get(self, request, id=None):
        if id:
            try:
                item = Library.objects.get(id=id)
                serializer = LibrarySerializer(item)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Library.DoesNotExist:
                return Response(data=None, status=status.HTTP_404_NOT_FOUND)

        items = Library.objects.all()
        serializer = LibrarySerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = LibrarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_303_SEE_OTHER, headers={"location": "/library/" + str(serializer.data['id'])})
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
