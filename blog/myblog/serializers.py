from rest_framework import serializers

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True # пароль не может быть прочитан клиентской стороной
    )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'quote', 'password', 'token']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    # метод update определён в базовом классе
