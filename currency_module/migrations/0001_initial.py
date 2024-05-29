# Generated by Django 5.0.6 on 2024-05-29 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CountryCurrencies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(max_length=50, unique=True)),
                ('currency_name', models.CharField(default='Нет единой валюты', max_length=50)),
                ('currency_code', models.CharField(max_length=3, null=True)),
                ('currency_number', models.CharField(max_length=3)),
            ],
            options={
                'db_table': 'country_currencies',
            },
        ),
        migrations.CreateModel(
            name='ExchangeRates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('currency', models.CharField(max_length=10)),
                ('date', models.DateField()),
                ('value', models.DecimalField(decimal_places=4, max_digits=100)),
                ('daily_change', models.DecimalField(decimal_places=4, max_digits=100)),
            ],
            options={
                'db_table': 'echange_rates',
                'unique_together': {('currency', 'date')},
            },
        ),
    ]