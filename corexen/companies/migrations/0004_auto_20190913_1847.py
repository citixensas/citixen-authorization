# Generated by Django 2.2.4 on 2019-09-13 23:47

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_headquarter_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
        migrations.AddField(
            model_name='headquarter',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
    ]