# Generated by Django 4.1.7 on 2023-04-21 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_post_file_post_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='video',
            field=models.FileField(blank=True, upload_to='videos/'),
        ),
    ]