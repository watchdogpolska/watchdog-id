from django.contrib.auth.models import Group
from rest_framework import serializers
from watchdog_id.users.models import User
from django.utils.encoding import force_text


class UserSerializer(serializers.ModelSerializer):
    visible_name = serializers.SerializerMethodField()
    absolute_url = serializers.SerializerMethodField()

    def get_visible_name(self, obj):
        return force_text(obj)

    def get_absolute_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.get_absolute_url())

    class Meta:
        fields = ['username', 'name', 'absolute_url', 'visible_name']
        model = User


class UserSelfSerializer(UserSerializer):
    class Meta:
        fields = UserSerializer.Meta.fields + ['email', ]
        model = User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['name', ]
        model = Group
