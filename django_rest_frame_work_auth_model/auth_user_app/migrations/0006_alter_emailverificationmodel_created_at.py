# Generated by Django 4.1.2 on 2022-10-28 06:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_user_app', '0005_alter_emailverificationmodel_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverificationmodel',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 28, 6, 58, 30, 575024, tzinfo=datetime.timezone.utc)),
        ),
    ]
