# Generated by Django 2.2.3 on 2019-08-26 21:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('companies', '__latest__'),
        ('auth', '__latest__'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('-created_at', '-updated_at'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GroupTemplatePermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='permissions.GroupTemplate')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='auth.Permission')),
            ],
            options={
                'ordering': ('-created_at', '-updated_at'),
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='grouptemplate',
            name='group_permissions',
            field=models.ManyToManyField(blank=True, through='permissions.GroupTemplatePermission', to='auth.Permission', verbose_name='group_permissions'),
        ),
        migrations.AddField(
            model_name='grouptemplate',
            name='headquarter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='companies.Headquarter'),
        ),
        migrations.AddField(
            model_name='grouptemplate',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='permissions.GroupTemplate'),
        ),
    ]
