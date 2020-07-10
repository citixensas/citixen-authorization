# Generated by Django 3.0.8 on 2020-07-09 18:19

import corexen.utils.validators
import django.contrib.postgres.fields.citext
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200219_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=django.contrib.postgres.fields.citext.CIEmailField(blank=True, max_length=254, null=True, validators=[corexen.utils.validators.CorexenEmailValidator()], verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='non_verified_email',
            field=models.EmailField(blank=True, help_text='Verified email. This field is not used by all user profiles.', max_length=254, null=True, validators=[corexen.utils.validators.CorexenEmailValidator()], verbose_name='non email address'),
        ),
    ]
