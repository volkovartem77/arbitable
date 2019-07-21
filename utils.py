import datetime

from config import ERR_LOG_PATH, LOG_PATH


def log(text, symbol=''):
    file = open(LOG_PATH, "a")
    dt = datetime.datetime.now().replace(microsecond=0).isoformat().replace('T', ' ')
    file.write(dt + ' ' + symbol + ' ' + text + '\n')
    file.close()
    print(dt + ' ' + symbol + ' ' + text)


def err_log(text, symbol=''):
    file = open(ERR_LOG_PATH, "a")
    dt = datetime.datetime.now().replace(microsecond=0).isoformat().replace('T', ' ')
    file.write(dt + ' ' + symbol + '\n' + text + '\n')
    file.close()
    print(dt + ' ' + symbol + '\n' + text)