# Generated by Django 3.0.3 on 2020-04-06 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0005_auto_20200129_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='headquarter',
            name='google_key',
            field=models.CharField(max_length=120, null=True),
        ),
    ]
