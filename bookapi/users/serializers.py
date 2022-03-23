from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerilizer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)

    class Meta:
        model = User
        exclude = ('password', )