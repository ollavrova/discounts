from __future__ import unicode_literals
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.db import models

STATUS = (
        ('new', 'New'),
        ('active', 'Actice'),
        ('reconciliation', 'Reconciliation'),
        ('closed', 'Closed'),
    )


class Company(models.Model):
    name = models.CharField(max_length=256, unique=True, null=False)
    country = CountryField()


class Agreement(models.Model):
    negotiator = models.ForeignKey(User)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    company = models.ForeignKey(Company)
    export_amount = models.DecimalField(max_digits=15, default=0, decimal_places=2)
    import_amount = models.DecimalField(max_digits=15, default=0, decimal_places=2)


class Period(models.Model):
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    agreement = models.ForeignKey(Agreement)
    status = models.CharField(choices=STATUS, max_length=15, default='new')

