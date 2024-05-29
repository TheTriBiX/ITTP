from rest_framework.serializers import ModelSerializer
from .models import ExchangeRates, CountryCurrency


class ExchangeRatesSerializer(ModelSerializer):
    class Meta:
        model = ExchangeRates
        fields = ('currency', 'date', 'value', 'daily_change')


class CountryCurrencySerializer(ModelSerializer):
    class Meta:
        model = CountryCurrency
        fields = ('country_name', 'currency_name', 'currency_code', 'currency_number')