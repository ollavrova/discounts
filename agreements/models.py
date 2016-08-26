from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django_countries.fields import CountryField
from django.db import models
from django.utils.translation import ugettext_lazy as _

STATUS = (
        ('new', 'New'),
        ('active', 'Active'),
        ('reconciliation', 'Reconciliation'),
        ('closed', 'Closed'),
    )


class Company(models.Model):
    name = models.CharField(max_length=256, unique=True, null=False)
    country = CountryField()

    def __unicode__(self):
        return '{} {}'.format(self.name, self.country.alpha3)


class Agreement(models.Model):
    negotiator = models.ForeignKey(User)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    company = models.ForeignKey(Company)
    export_amount = models.DecimalField(max_digits=15, default=0, decimal_places=2)
    import_amount = models.DecimalField(max_digits=15, default=0, decimal_places=2)

    def __unicode__(self):
        return '{} of {} from {}'.format(self.negotiator.username, self.company.name, str(self.start_date))


class Period(models.Model):
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    agreement = models.ForeignKey(Agreement, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, max_length=15, default='new')

    def __unicode__(self):
        return '{} period of {} {}'.format(self.status, self.agreement, str(self.start_date))

    def clean(self):
        if self.start_date < self.agreement.start_date:
            raise ValidationError(
                _('Please input a valid start date, this one is not correct'),
                params={'value': self.start_date},
            )

        if self.end_date > self.agreement.end_date:
            raise ValidationError(
                _('Please input a valid end date, this one is not correct'),
                params={'value': self.end_date},
            )


