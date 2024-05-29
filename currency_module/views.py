import requests
from django.shortcuts import render
from .parser_module.parser import CurrencyParser, CurrencyCodesParser
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.db.utils import IntegrityError
from django.views.generic import View
import matplotlib
import matplotlib.pyplot as plt
from django.core.exceptions import ValidationError

matplotlib.use('agg')


class AllCurrencyAPI(APIView):
    def get(self, request):
        return Response({"currencies": ExchangeRatesSerializer(ExchangeRates.objects.all(), many=True).data})

    def post(self, request):
        date_from = request.data['date_from']
        date_to = request.data['date_to']
        currencies = CurrencyParser(*date_from.split('-')[::-1], *date_to.split('-')[::-1]).get_currency_by_period()
        for currency in currencies:
            for date in currencies[currency]:
                value = currencies[currency][date]['value']
                daily_change = currencies[currency][date]['daily_change']
                date = '-'.join(date.split('.')[::-1])
                try:
                    new_obj = ExchangeRates(currency=currency, date=date, value=value,
                                            daily_change=daily_change).save()
                except IntegrityError:
                    new_obj = ExchangeRates.objects.get(currency=currency, date=date)
                    new_obj.value = value
                    new_obj.daily_change = daily_change
                except ValidationError:
                    print("Invalid date")
            response = ExchangeRates.objects.filter(date__gte=date_from).filter(date__lte=date_to)
        return Response({"currencies": ExchangeRatesSerializer(response, many=True).data})


class ListOfAllCurrencies(APIView):
    def post(self, request):
        countries_codes = CurrencyCodesParser().get_data()
        for country in countries_codes:
            currency_name = countries_codes[country]['currency_name']
            currency_code = countries_codes[country]['currency_code']
            currency_number = countries_codes[country]['currency_number']

            try:
                new_obj = CountryCurrency(country_name=country, currency_name=currency_name,
                                          currency_code=currency_code,
                                          currency_number=currency_number).save()

            except IntegrityError:
                print("CountryCurrency alreasy exist, nothing to update")
        return Response({"countries": CountryCurrencySerializer(CountryCurrency.objects.all(), many=True).data})

    def get(self, request):
        return Response({"countries": CountryCurrencySerializer(CountryCurrency.objects.all(), many=True).data})


class InterfaceView(View):
    def __init__(self):
        self.days = [_ for _ in range(1, 32)]
        self.month = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь',
                      'ноябрь', 'декабрь']
        self.years = [_ for _ in range(1992, 2025)]

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html', {'days': self.days, 'month': self.month, 'years': self.years})

    def post(self, request, *args, **kwargs):
        day_from = request.POST['day_from']
        day_to = request.POST['day_to']

        month_from = self.month.index(request.POST['month_from']) + 1
        month_to = self.month.index(request.POST['month_to']) + 1

        year_from = request.POST['year_from']
        year_to = request.POST['year_to']
        data = {'date_from': f'{year_from}-{month_from}-{day_from}',
                'date_to': f'{year_to}-{month_to}-{day_to}'}
        headers = {"Content-Type": "application/json; charset=utf-8"}
        response = requests.post(url='http://127.0.0.1:8000/api/v1/currency-by-data/', json=data, headers=headers)
        if response.status_code == 200:
            response = response.json()['currencies']
        else:
            print(data, response.status_code)
        return render(request, 'index.html',
                      {'days': self.days, 'month': self.month, 'years': self.years, 'table': response})


def create_graphic(countries, date_from, date_to):
    res = []
    for country in countries:
        path = f'media/{country}-{date_from}-{date_to}.png'
        try:

            img = open(path)
            res.append(f'{country}-{date_from}-{date_to}.png')
        except FileNotFoundError:
            value, date = zip(*countries[country])
            plt.plot(list(date), list(value))
            plt.ylabel('Стоимость (руб)')
            plt.xlabel('Дата')
            plt.xticks(rotation=90)
            plt.suptitle(country)
            plt.savefig(path)
            res.append(f'{country}-{date_from}-{date_to}.png')
        plt.close()
    return res


class GraphicsView(View):
    def __init__(self):
        self.days = [_ for _ in range(1, 32)]
        self.month = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль', 'август', 'сентябрь', 'октябрь',
                      'ноябрь', 'декабрь']
        self.years = [_ for _ in range(1992, 2025)]
        self.countries = ExchangeRates.objects.values('currency').distinct()

    def get(self, request):
        return render(request, 'graphix.html',
                      {'days': self.days, 'month': self.month, 'years': self.years, 'countries': self.countries})

    def post(self, request):
        countries = ExchangeRates.objects.values('currency').distinct()
        selected_countries = dict()
        for country in request.POST:
            if request.POST[country] == 'on':
                selected_countries[country] = ''

        day_from = request.POST['day_from']
        day_to = request.POST['day_to']

        month_from = self.month.index(request.POST['month_from']) + 1
        month_to = self.month.index(request.POST['month_to']) + 1

        year_from = request.POST['year_from']
        year_to = request.POST['year_to']

        date_from = f'{year_from}-{month_from}-{day_from}'
        date_to = f'{year_to}-{month_to}-{day_to}'

        data = {'date_from': date_from,
                'date_to': date_to}
        headers = {"Content-Type": "application/json; charset=utf-8"}
        response = requests.post(url='http://127.0.0.1:8000/api/v1/currency-by-data/', json=data, headers=headers)
        for country in selected_countries:
            selected_countries[country] = [(float(obj.value), str(obj.date)) for obj in
                                           ExchangeRates.objects.filter(currency=country).filter(
                                               date__gte=date_from).filter(date__lte=date_to)]
        graphics = create_graphic(selected_countries, date_from, date_to)
        print(graphics)
        return render(request, 'graphix.html',
                      {'days': self.days, 'month': self.month, 'years': self.years, 'graphics': graphics,
                       'countries': self.countries})
