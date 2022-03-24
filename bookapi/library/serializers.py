from rest_framework import serializers

from transactions.models import Transaction

from .models import Library

class LibrarySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)
    address = serializers.CharField(max_length=200)
    city = serializers.CharField(max_length=200)
    state = serializers.CharField(max_length=2)
    zip = serializers.CharField(max_length=5)

    class Meta:
        model = Library
        fields = ('__all__')