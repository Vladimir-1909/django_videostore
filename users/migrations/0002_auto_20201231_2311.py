# Generated by Django 3.1.4 on 2020-12-31 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='img',
            field=models.ImageField(default='default-user.png', upload_to='user_images'),
        ),
    ]
