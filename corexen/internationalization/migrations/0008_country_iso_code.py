# Generated by Django 3.0.8 on 2022-10-14 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internationalization', '0007_auto_20200406_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='iso_code',
            field=models.CharField(default=None, max_length=6),
        ),
    ]
