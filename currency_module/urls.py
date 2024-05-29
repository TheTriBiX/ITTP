from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('currency-by-data/', AllCurrencyAPI().as_view()),
    path('country-currencies/', ListOfAllCurrencies.as_view())
]
