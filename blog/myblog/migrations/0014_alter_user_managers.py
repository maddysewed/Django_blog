# Generated by Django 4.1.4 on 2023-03-13 07:09

from django.db import migrations
import myblog.models


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0013_alter_user_options_remove_user_created_at_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', myblog.models.MyUserManager()),
            ],
        ),
    ]
