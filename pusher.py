import json
import threading
import time
import traceback

import requests

from config import DATABASE, TIMEOUT_PUSH, EXCHANGES, BANK_RATE


def convert_symbol(symbol):
    if symbol == 'THB_BTC':
        return '1'
    if symbol == 'THB_ETH':
        return '21'


def push_bank_rate():
    while True:
        r = requests.get('https://www.krungsri.com/bank/en/Other/ExchangeRate/Todayrates.html')
        if r is not None:
            bank_rate = r.text.split("</td></tr><tr style='background-color:transparent !important'>")[0].split('>')[-1]
            DATABASE.set(BANK_RATE, bank_rate)
            # print(bank_rate)
        time.sleep(TIMEOUT_PUSH)


def push_bxin_tick(symbol):
    while True:
        r = requests.get(f"https://bx.in.th/api/orderbook/?pairing={convert_symbol(symbol)}")
        if r is not None:
            r = json.loads(r.text)
            bid = round(float(r['bids'][0][0]), 2)
            ask = round(float(r['asks'][0][0]), 2)
            bid_amount = float(r['bids'][0][1])
            ask_amount = float(r['asks'][0][1])
            # print(symbol, '  ', bid, bid_amount, '    ', ask, ask_amount)
            DATABASE.set('bxin_' + symbol, json.dumps({
                'ask': ask,
                'bid': bid,
                'ask_amount': ask_amount,
                'bid_amount': bid_amount
            }))
            # print(DATABASE.get('bxin_' + symbol))
        time.sleep(TIMEOUT_PUSH)


def push_itbit_tick(symbol):
    while True:
        r = requests.get(f"https://api.itbit.com/v1/markets/{symbol.replace('_', '')}/ticker")
        if r is not None:
            r = json.loads(r.text)
            DATABASE.set('itbit_' + symbol, json.dumps({
                'ask': float(r['ask']),
                'bid': float(r['bid']),
                'ask_amount': float(r['askAmt']),
                'bid_amount': float(r['bidAmt'])
            }))
            # print(DATABASE.get('itbit_' + symbol))
        time.sleep(TIMEOUT_PUSH)


def launch():
    for symbol in EXCHANGES['itbit']:
        th_itbit = threading.Thread(target=push_itbit_tick, kwargs={"symbol": symbol})
        th_itbit.start()
    for symbol in EXCHANGES['bxin']:
        th_bxin = threading.Thread(target=push_bxin_tick, kwargs={"symbol": symbol})
        th_bxin.start()
    th_bank_rate = threading.Thread(target=push_bank_rate)
    th_bank_rate.start()
    print('pusher start')


if __name__ == "__main__":
    try:
        launch()
    except KeyboardInterrupt:
        exit()
    except:
        print(traceback.format_exc())
