from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.views.generic import ListView, DetailView, View
from django.core.exceptions import ObjectDoesNotExist
from sharestockdata.models import StockInfo
# from sharestockdata.serializers import PostSerializer
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import mixins
from rest_framework import generics
from django.contrib.auth.models import User
from sharestockdata.serializers import UserSerializer
from rest_framework import permissions
from sharestockdata.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from .forms import *
import random
from django.contrib import messages
from .models import testData


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'posts': reverse('post-list', request=request, format=format)
    })


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# class PostList(generics.ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#
# class PostDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

def random_for_max(minorder):
    a=random.randint(100,201)
    if a>minorder:
        return a
    else:
        a=random.randint(100,201)


class testdata(View):
    def get(self, *args, **kwargs):
        form = DataForm()
        context = {
            'form': form
        }
        return render(self.request, 'test.html', context)

    def post(self, *args, **kwargs):
        form = DataForm(self.request.POST or None)
        minorder=random.randint(100,200)
        if form.is_valid():
            day = form.cleaned_data.get('daydata')
            changelimit = form.cleaned_data.get('changelimit')

            try:
                # do something
                test_data=testData(
                    day=day,
                    min_order=minorder,
                    max_order=random_for_max(minorder),
                    volume=random.choice([10,100,1000]),
                    change_limit=changelimit
                )
                test_data.save()
                messages.info(self.request, 'good')
                return redirect('sharestockdata:test-data')
            except ObjectDoesNotExist:
                messages.info(self.request, 'fail')
                return redirect('sharestockdata:test-data')
