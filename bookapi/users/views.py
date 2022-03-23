from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerilizer
from django.contrib.auth.models import User

# Create your views here.
class UserViews(APIView):
    def get(self, request, id=None):
        if id:
            try:
                item = User.objects.get(id=id)
                serializer = UserSerilizer(item)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response(data=None, status=status.HTTP_404_NOT_FOUND)

        items = User.objects.all()
        serializer = UserSerilizer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)