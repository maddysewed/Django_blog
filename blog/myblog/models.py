from django.db import models
import datetime
from django.urls import reverse
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserManager(BaseUserManager):

    def create_user(self, username, email, password):
        """ Создает и возвращает пользователя с имэйлом, паролем и именем. """
        if email is None:
            raise TypeError('У пользователя должен быть имейл')

        if password is None:
            raise TypeError('У пользователя должен быть пароль')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        """ Создает и возввращет пользователя с привилегиями суперадмина. """

        if email is None:
            raise TypeError('У суперпользователя должен быть имейл')

        if password is None:
            raise TypeError('У суперпользователя должен быть пароль')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, blank=False, on_delete=models.CASCADE,)
    quote = models.CharField(max_length=300, blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, verbose_name="Avatar")  # year, month, day

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def __str__(self):
        return self.user.username


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200, db_index=True)
    content = models.TextField(blank=True)  # blank=True  поле не обязательно к заполнению
    date = models.DateTimeField(auto_now_add=True)
    tag = models.ForeignKey("Tag", on_delete=models.PROTECT)
    favorite = models.ManyToManyField(User, related_name='post_favourite', blank=True)

    def __str__(self):
        return self.title

# class Favorite(models.Model):
#     user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='favorites')
#     post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='favorites')


class Tag(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name="Tag name")

    def get_absolute_url(self):
        return reverse("tags", kwargs={"tag_id": self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ("name", )
