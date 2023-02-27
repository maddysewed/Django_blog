from django.shortcuts import render, get_object_or_404, redirect

from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsOwnerOrReadOnly
from .serializers import (
    RegistrationSerializer,
    #LoginSerializer,
    ProfileSerializer,
    PostSerializer,
    TagSerializer,
)

from .models import Profile, User, Post, Tag
from django.contrib.auth import login, logout



# class UserFavoriteDetail(generics.RetrieveAPIView):
#     queryset = Favorite.objects.all()
#     serializer_class = FavoritesSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly,
#                           IsOwnerOrReadOnly]
#
#
# class FavoritesList(generics.ListAPIView):
#     queryset = Favorite.objects.all()
#     serializer_class = FavoritesSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


class PostFavoriteView(APIView):
    bad_request_message = 'An error has occurred'

    # def get(self, request):
    #     queryset = Post.objects.all()
    #     serializer_class = PostSerializer
    #     permission_classes = [permissions.IsAuthenticatedOrReadOnly,
    #                           IsOwnerOrReadOnly]

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


class TagDetailList(generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagList(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]


class UserProfileDetail(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserList(generics.ListAPIView): # список пользователей (только для чтения)
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer


class UserDetail(generics.RetrieveAPIView): # доступ к одному пользователю
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer


