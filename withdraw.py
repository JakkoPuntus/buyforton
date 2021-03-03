import requests
import time
import hmac
import hashlib
import json
import logging

def send_ton(address, amount):

    data = {
        'withdraw_type': 'ton',
        'amount': amount,
        'address': address,
        'payment_id': "from buyforton",
        'withdrawall': True
    }

    key = 'pXGToH2CFBPkDBF1sPXpG74UabUB8TEUfK98zYal'
    key = key.encode('ascii')

    body = json.dumps(data)
    nonce =  str(int(time.time()*1000.0))
    api_path = '/v3/auth/withdraw'
    
    signature_string = api_path + nonce + body


    signature = hmac.new(key, signature_string.encode('ascii'), hashlib.sha384 ).hexdigest()
  
    headers = {
    'accept': 'application/json',
    'content-type': 'application/json',
    'kun-nonce': nonce,
    'kun-apikey': 'qBvJaMi0QcLmxMX5wiab2kuJxFSOi2cU8LvxTVZn',
    'kun-signature': signature
    }
    
    print(body)
    logging.basicConfig(level=logging.DEBUG)
    response = requests.post('https://api.kuna.io/v3/auth/withdraw', headers=headers, data=body)
    return response
