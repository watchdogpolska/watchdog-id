from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from watchdog_id.users.models import User

from .serializers import GroupSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @list_route()
    def me(self, request, *args, **kwargs):
        self.object = get_object_or_404(User, pk=request.user.id)
        serializer = self.get_serializer(self.object)
        return Response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
