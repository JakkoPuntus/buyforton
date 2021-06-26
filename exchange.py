import requests
import ast

def get_exchange_rub():
    headers = {'ids': 'ton-crystal', 'vs_currencies': 'rub'}
    response = requests.get('https://api.coingecko.com/api/v3/simple/price', params=headers)
    return ast.literal_eval(response.text)['ton-crystal']['rub']


def get_exchange_usd():
    headers = {'ids': 'ton-crystal', 'vs_currencies': 'usd'}
    response = requests.get('https://api.coingecko.com/api/v3/simple/price', params=headers)
    return ast.literal_eval(response.text)['ton-crystal']['usd']

print(get_exchange_usd())