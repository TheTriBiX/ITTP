# Generated by Django 5.0.6 on 2024-05-29 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency_module', '0003_rename_countrycurrencies_countrycurrency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exchangerates',
            name='date',
            field=models.DateField(),
        ),
    ]
