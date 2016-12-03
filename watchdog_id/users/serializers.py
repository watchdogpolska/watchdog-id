from django.contrib.auth.models import Group
from rest_framework import serializers
from watchdog_id.users.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ['username', ]
        model = User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', ]
        model = Group
