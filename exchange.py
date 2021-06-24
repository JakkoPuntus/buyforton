import requests

def get_exchange():
    headers = {'api-key': 'Ki0U3HWIMoPrNpi'}
    response = requests.get('https://api.broxus.com/v1/meta/currencies_pairs', headers=headers)
    return response

print(get_exchange())