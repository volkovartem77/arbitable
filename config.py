import json
import os

import redis as redis

# os.path.abspath(os.curdir)
PROJECT_PATH = os.path.abspath(os.curdir) + '/'
PROJECT_FOLDER = PROJECT_PATH.split('/')[-2]
CONF_PATH = PROJECT_PATH + PROJECT_FOLDER + '.conf'


def get_preferences():
    ff = open(PROJECT_PATH + 'preferences.txt', "r")
    preferences = json.loads(ff.read())
    ff.close()
    return preferences


EXCHANGES = get_preferences()['exchanges']
SYMBOLS = get_preferences()['exchanges']['itbit'] + get_preferences()['exchanges']['bxin']

DATABASE = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)


# Constants
TIMEOUT_PUSH = 1
BANK_RATE = 'BANK_RATE'
