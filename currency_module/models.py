from django.db import models


class ExchangeRates(models.Model):
    class Meta:
        db_table = 'echange_rates'
        unique_together = ('currency', 'date')

    currency = models.CharField(max_length=10)
    date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=4)
    daily_change = models.DecimalField(max_digits=10, decimal_places=4)


class CountryCurrency(models.Model):
    class Meta:
        db_table = 'country_currencies'

    country_name = models.CharField(max_length=50, unique=True)
    currency_name = models.CharField(max_length=50, default='Нет единой валюты')
    currency_code = models.CharField(max_length=3, null=True)
    currency_number = models.CharField(max_length=3)

#
# class DefaultCountryCurrency(models.Model):
#     country_name = models.CharField(max_length=50)

