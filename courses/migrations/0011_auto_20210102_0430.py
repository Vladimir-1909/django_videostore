# Generated by Django 3.1.4 on 2021-01-01 23:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_auto_20210102_0400'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='avtor_comment',
            new_name='author',
        ),
        migrations.RenameField(
            model_name='lesson',
            old_name='avtor',
            new_name='author',
        ),
    ]
