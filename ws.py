import json
import random
import threading
import time

from simple_websocket_server import WebSocketServer, WebSocket

from config import DATABASE, BANK_RATE
from utils import log

ths = {}


def get_data():
    bidask1 = json.loads(DATABASE.get('itbit_XBT_USD'))
    bidask2 = json.loads(DATABASE.get('itbit_ETH_USD'))
    bidask3 = json.loads(DATABASE.get('bxin_THB_BTC'))
    bidask4 = json.loads(DATABASE.get('bxin_THB_ETH'))

    bank_rate = float(str(DATABASE.get(BANK_RATE)))

    return [
        {
            "exchange": "ITBIT",
            "symbol": "XBT_USD",
            "bid": str(bidask1['bid']),
            "bid_amount": '{0:.8f}'.format(bidask1['bid_amount']),
            "ask": str(bidask1['ask']),
            "ask_amount": '{0:.8f}'.format(bidask1['ask_amount']),
            "bank_rate": str(bank_rate),
            "diff": str(round(bidask3['bid'] / bank_rate / bidask1['ask'] * 100 - 100, 2))
        },
        {
            "exchange": "BXIN",
            "symbol": "THB_BTC",
            "bid": str(bidask3['bid']),
            "bid_amount": str(bidask3['bid_amount']),
            "ask": str(bidask3['ask']),
            "ask_amount": str(bidask3['ask_amount']),
            "bank_rate": str(bank_rate),
            "diff": ""
        },
        {
            "exchange": "ITBIT",
            "symbol": "ETH_USD",
            "bid": str(bidask2['bid']),
            "bid_amount": str(bidask2['bid_amount']),
            "ask": str(bidask2['ask']),
            "ask_amount": str(bidask2['ask_amount']),
            "bank_rate": str(bank_rate),
            "diff": str(round(bidask4['bid'] / bank_rate / bidask2['ask'] * 100 - 100, 2))
        },
        {
            "exchange": "BXIN",
            "symbol": "THB_ETH",
            "bid": str(bidask4['bid']),
            "bid_amount": str(bidask4['bid_amount']),
            "ask": str(bidask4['ask']),
            "ask_amount": str(bidask4['ask_amount']),
            "bank_rate": str(bank_rate),
            "diff": ""
        }
    ]


def get_test_data():
    bid1 = random.randrange(9600, 9700)
    ask1 = random.randrange(9700, 9800)
    bid2 = random.randrange(12000, 12400)
    ask2 = random.randrange(12450, 12800)
    bid3 = random.randrange(309000, 310000)
    ask3 = random.randrange(310000, 311000)
    bid4 = random.randrange(12000, 12400)
    ask4 = random.randrange(12450, 12800)
    bid_amount1 = round(random.uniform(0, 1), 2)
    ask_amount1 = round(random.uniform(0, 1), 2)
    bid_amount2 = round(random.uniform(0, 1), 2)
    ask_amount2 = round(random.uniform(0, 1), 2)
    bid_amount3 = round(random.uniform(0, 1), 2)
    ask_amount3 = round(random.uniform(0, 1), 2)
    bid_amount4 = round(random.uniform(0, 1), 2)
    ask_amount4 = round(random.uniform(0, 1), 2)

    bank_rate = float(str(DATABASE.get(BANK_RATE)))

    return [
        {
            "exchange": "ITBIT",
            "symbol": "XBT_USD",
            "bid": str(bid1),
            "bid_amount": str(bid_amount1),
            "ask": str(ask1),
            "ask_amount": str(ask_amount1),
            "bank_rate": str(bank_rate),
            "diff": str(round(bid3 / bank_rate / ask1 * 100 - 100, 2))
        },
        {
            "exchange": "ITBIT",
            "symbol": "ETH_USD",
            "bid": str(bid2),
            "bid_amount": str(bid_amount2),
            "ask": str(ask2),
            "ask_amount": str(ask_amount2),
            "bank_rate": str(bank_rate),
            "diff": str(round(bid4 / bank_rate / ask2 * 100 - 100, 2))
        },
        {
            "exchange": "BXIN",
            "symbol": "THB_BTC",
            "bid": str(bid3),
            "bid_amount": str(bid_amount3),
            "ask": str(ask3),
            "ask_amount": str(ask_amount3),
            "bank_rate": str(bank_rate),
            "diff": str(round(bid1 / bank_rate / ask3 * 100 - 100, 2))
        },
        {
            "exchange": "BXIN",
            "symbol": "THB_ETH",
            "bid": str(bid4),
            "bid_amount": str(bid_amount4),
            "ask": str(ask4),
            "ask_amount": str(ask_amount4),
            "bank_rate": str(bank_rate),
            "diff": str(round(bid2 / bank_rate / ask4 * 100 - 100, 2))
        }
    ]


class SimpleEcho(WebSocket):
    def update(self, th_id):
        global ths
        while ths[th_id]:
            print('{} Update chart: {}'.format(self.address[1], json.dumps(get_data())))
            self.send_message(json.dumps(get_data()))
            time.sleep(1)

    def handle(self):
        pass

    def connected(self):
        print(self.address[1], 'connected')
        th = threading.Thread(target=self.update, kwargs={"th_id": self.address[1]})
        global ths
        ths[self.address[1]] = True
        th.start()

    def handle_close(self):
        print(self.address[1], 'closed')
        global ths
        ths[self.address[1]] = False


log('websocket start')
server = WebSocketServer('', 9999, SimpleEcho)
server.serve_forever()
