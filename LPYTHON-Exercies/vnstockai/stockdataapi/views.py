from django.contrib.auth.models import User, Group
from django.shortcuts import render
from .serializers import UserSerializer, GroupSerializer
# Create your views here.


# ViewSets define the view behavior.
from rest_framework import viewsets, permissions


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


#     add, edit, delete


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

