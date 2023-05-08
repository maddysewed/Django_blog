from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile, Tag, Post


# admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Post)
