import pytz
import sys
import requests
import datetime

def get_local_time ():
    utc_now = datetime.datetime.utcnow()
    tz = pytz.timezone('Asia/Shanghai')
    local_t = utc_now.replace(tzinfo=pytz.utc).astimezone(tz)
    return local_t.strftime('%Y-%m-%d %H:%M:%S')

def get_exchanger_price (exchanger, pair):
    if exchanger == 'btce':
        return get_btce_price (pair)
    elif exchanger == 'yunbi':
        return get_yunbi_price (pair)
    elif exchanger == 'chbtc':
        return get_chbtc_price (pair)
    elif exchanger == 'bitstamp':
        return get_bitstamp_price (pair)
    else:
        raise ('exchanger name not found!')
    

def get_btce_price(pair='btc_usd'):
    url = 'https://btc-e.com/api/3/ticker/' + pair
    r = requests.get(url=url)
    btce_json = r.json()
    btce_price = btce_json[pair]['last']
    return get_local_time (), float(btce_price)

def get_yunbi_price(pair='btccny'):
    if pair  == 'btc_cny':
        pair = 'btccny'
    elif pair == 'eth_cny':
        pair = 'ethcny'

        
    url = 'https://yunbi.com/api/v2/tickers/' + pair + '.json'

    r = requests.get(url=url)

    yb_json = r.json()

    yb_price = yb_json['ticker']['last']

    return get_local_time (), float(yb_price)

def get_chbtc_price (pair='btc_cny'):
    url = 'http://api.chbtc.com/data/v1/ticker?currency=' + pair
    r = requests.get (url = url)
    j = r.json ()
    price = j ['ticker'] ['last']
    return get_local_time (), float (price)

def get_bitstamp_price(pair='btcusd'):
    if pair == 'btc_cny':
        pair = 'btcusd'
    elif pair == 'ltc_cny':
        pair = 'ltcusd'
    elif pair == 'eth_cny':
        pair = 'ethusd'

    url = 'https://www.bitstamp.net/api/v2/ticker/' + pair

    r = requests.get (url = url)

    j = r.json ()
    price = j ['last']

    return get_local_time (), float (price)
