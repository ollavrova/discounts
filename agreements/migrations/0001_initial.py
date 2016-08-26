# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


def create_admin(apps, schema_editor):
    user = apps.get_model('auth', 'User')
    admin = user(username='admin',
                 password=make_password('adminadmin'),
                 email='admin@example.com',
                 is_superuser=True,
                 is_staff=True
                 )
    admin.save()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agreement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('export_amount', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
                ('import_amount', models.DecimalField(decimal_places=2, default=0, max_digits=15)),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('status', models.CharField(choices=[('new', 'New'), ('active', 'Actice'), ('reconciliation', 'Reconciliation'), ('closed', 'Closed')], default='new', max_length=15)),
                ('agreement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agreements.Agreement')),
            ],
        ),
        migrations.AddField(
            model_name='agreement',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='agreements.Company'),
        ),
        migrations.AddField(
            model_name='agreement',
            name='negotiator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunPython(create_admin),
    ]
