# Generated by Django 4.1.4 on 2023-02-24 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0011_alter_favorite_post_alter_favorite_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Favorite',
        ),
    ]
