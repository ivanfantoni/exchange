from urllib.request import urlopen
from urllib import parse
import json
from typing import Union


class Exchange:

    def __init__(self, from_currency:str ='EUR', to_currency:str = None, amount:Union[int,float]=1):
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.amount = amount


    def convert(self):
        self.params = {
            'from':self.from_currency.upper(),
            'to':self.to_currency.upper(),
            'amount':self.amount
        }

        query_string = parse.urlencode(self.params)

        url = f'https://api.exchangerate.host/convert?{query_string}'
        resp = urlopen(url).read().decode('utf-8')
        result = json.loads(resp)
        return result
    

    def latest_rate(self):
        self.params = {
            'base':self.from_currency,
            'amount':self.amount
        }
        query_string = parse.urlencode(self.params)

        url = f'https://api.exchangerate.host/latest?{query_string}'
        resp = urlopen(url).read().decode('utf-8')
        result = json.loads(resp)
        return result


    @staticmethod
    def symbols():
        url = f'https://api.exchangerate.host/symbols'
        resp = urlopen(url).read().decode('utf-8')
        results = json.loads(resp)
        codes = results['symbols']
        return codes


    def currency_codes(self):
        codes = self.symbols()
        for result in codes.values():
            print(f'Description: {result["description"]} - Code: {result["code"]}')
