from django.db import models
import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import UserManager


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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200, db_index=True)
    content = models.TextField(blank=True)  # blank=True  поле не обязательно к заполнению
    date = models.DateTimeField(auto_now_add=True)
    tag = models.ForeignKey("Tag", on_delete=models.PROTECT)
    favorite = models.ManyToManyField(User, related_name='post_favourite', blank=True)

    def __str__(self):
        return self.title


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
