# Generated by Django 4.1.7 on 2023-05-09 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_likepost'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='no_of_likes',
            field=models.IntegerField(default=0),
        ),
    ]
