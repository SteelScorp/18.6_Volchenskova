import requests
import json
from config import currency


class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f"Невозможно конвертировать одинаковые валюты {quote}={base}.")

        try:
            quote_ticker = currency[quote]
        except KeyError:
            raise ConvertionException(f"Не удалось конвертировать валюту: {quote}")

        try:
            base_ticker = currency[base]
        except KeyError:
            raise ConvertionException(f"Не удалось конвертировать валюту: {base}")

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f"Не удалось распознать количество: {amount}")

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[currency[base]]

        return total_base
