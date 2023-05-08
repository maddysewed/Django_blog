from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import Profile, Post, Tag


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True # пароль не может быть прочитан клиентской стороной
    )

    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'posts', 'post_favourite']


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    # метод update определён в базовом классе


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Profile
        fields = ['photo', 'quote', 'user']


# class LoginSerializer(serializers.Serializer):
#     email = serializers.CharField(max_length=255)
#     username = serializers.CharField(max_length=255, read_only=True)
#     password = serializers.CharField(max_length=128, write_only=True)
#     token = serializers.CharField(max_length=255, read_only=True)
#
#     def validate(self, data):
#         email = data.get('email', None)
#         password = data.get('password', None)
#
#         if email is None:
#             raise serializers.ValidationError(
#                 'An email address is required to log in.'
#             )
#
#         if password is None:
#             raise serializers.ValidationError(
#                 'A password is required to log in.'
#             )
#
#         # Метод authenticate предоставляется Django и выполняет проверку, что
#         # предоставленные почта и пароль соответствуют какому-то пользователю в
#         # нашей базе данных
#         user = authenticate(username=email, password=password)
#
#         if user is None:
#             raise serializers.ValidationError(
#                 'A user with this email and password was not found.'
#             )
#
#         if not user.is_active:
#             raise serializers.ValidationError(
#                 'This user has been deactivated.'
#             )
#
#         # Метод validate должен возвращать словарь проверенных данных. Это
#         # данные, которые передются в т.ч. в методы create и update.
#         return {
#             'email': user.email,
#             'username': user.username,
#             'token': user.token
#         }


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'date', 'tag', 'author', 'favorite']


class TagSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ['name', 'posts']


# class FavoritesSerializer(serializers.ModelSerializer):
#     owner = serializers.ReadOnlyField(source='user.username')
#
#     class Meta:
#         model = Favorite
#         fields = ['post', 'owner', 'post']

    # a particular user's favorite movies:
    # user = User.objects.get(id='the_user_id')
    # user.favorites.values('movie')
