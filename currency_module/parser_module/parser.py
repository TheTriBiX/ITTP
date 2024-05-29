import requests
from bs4 import BeautifulSoup

currency_id = {
    "USD": 52148,
    "EUR": 52170,
    "GBP": 52146,
    "JPY": 52246,
    "TRY": 52158,
    "INR": 52238,
    "CNY": 52207,

}


class CurrencyParser:

    def __init__(self, bd: str, bm: str, by: str, ed: str, em: str, ey: str):
        self.__base_url = \
            f'https://www.finmarket.ru/currency/rates/?id=10148&pv=1&bd={bd}&bm={bm}&by={by}&ed={ed}&em={em}&ey={ey}&x=24&y=13'

    def get_currency_by_day(self):
        url = 'https://www.finmarket.ru/currency/rates/?id=10148&pv=0&bd=1&bm=1&by=2014&x=25&y=2#archive'
        default_currency = dict()
        request = requests.get(url=url)
        soup = BeautifulSoup(request.content, 'lxml')
        rows = soup.find_all('tr')

        for row in rows[2::]:
            currency_code, currency_name, currency_count, currency_value, *_ = row.find_all('td')
            default_currency[currency_code.text] = {'currency_name': currency_name.find('a').text,

                                                    'currency_value': float(currency_value.text.replace(',', '.'))
                                                                      / int(currency_count.text.replace(' ', '')),
                                                    }
        return default_currency

    def get_currency_by_period(self):
        currency = dict()
        for country in currency_id:
            result = dict()
            url = self.__base_url + f'&cur={currency_id[country]}'
            request = requests.get(url=url)
            soup = BeautifulSoup(request.content, 'lxml')
            rows = soup.tbody.find_all('tr')

            for row in rows:
                date, count, value, daily_change = row.find_all('td')
                result[date.text] = {"value": float(value.text.replace(',', '.')),
                                     "daily_change": float(daily_change.text.replace(',', '.'))}

            currency[country] = result

        return currency


class CurrencyCodesParser:
    def __init__(self):
        self._url = 'https://www.iban.ru/currency-codes'

    def get_data(self):
        request = requests.get(self._url)
        soup = BeautifulSoup(request.content, 'lxml')
        table = soup.find('table')
        rows = table.find_all('tr')[1::]
        response = dict()
        for row in rows:
            country, currency_name, currency_code, currency_number = row.find_all('td')
            response[country.text] = {'currency_name': currency_name.text,
                                      'currency_code': currency_code.text,
                                      'currency_number': currency_number.text,
                                      }
        return response
