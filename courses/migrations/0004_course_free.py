# Generated by Django 3.1.4 on 2020-12-31 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_auto_20201231_0234'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='free',
            field=models.BooleanField(default=True),
        ),
    ]
