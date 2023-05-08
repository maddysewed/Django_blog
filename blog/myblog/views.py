from django.shortcuts import render, get_object_or_404, redirect

from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView

from .permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import (
    RegistrationSerializer,
    ProfileSerializer,
    PostSerializer,
    TagSerializer,
)

from .models import Profile, Post, Tag
from django.contrib.auth import login, logout
from django.contrib.auth.models import User

# from djoser.views import UserViewSet
from rest_framework.response import Response


class PostFavoriteView(APIView):
    bad_request_message = 'An error has occurred'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.user not in post.favorite.all():
            post.favorite.add(request.user)
            return Response({'detail': 'User added to post'}, status=status.HTTP_200_OK)
        return Response({'detail': self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if request.user in post.favorite.all():
            post.favorite.remove(request.user)
            return Response({'detail': 'User removed from post'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': self.bad_request_message}, status=status.HTTP_400_BAD_REQUEST)


class TagDetailList(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly, IsAuthenticatedOrReadOnly]


class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]


class UserProfileDetail(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]


class UserList(generics.ListAPIView): # список пользователей (только для чтения)
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer


class UserDetail(generics.RetrieveAPIView): # доступ к одному пользователю
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
