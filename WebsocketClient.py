""" An example for Python Socket.io Client
    Requires: six,socketIO_client    
""" 
from socketIO_client import SocketIO, BaseNamespace
import json
import time
import re
import hmac
import hashlib
import base64

import logging
logging.getLogger('socketIO-client').setLevel(logging.DEBUG)


access_key = "<YOUR-ACCESS-KEY>"
secret_key = "<YOUE-SECRET-KEY>"

def get_tonce():
        return int(time.time() * 1000000)

def get_postdata():
        post_data = {}
        tonce = get_tonce()
        post_data['tonce'] = tonce
        post_data['accesskey'] = access_key
        post_data['requestmethod'] = 'post'

        if 'id' not in post_data:
                post_data['id'] = tonce

        #modefy here to meet your requirement
        post_data['method'] = 'subscribe'
        post_data['params'] = ['order_cnybtc', 'order_cnyltc', 'order_btcltc', 'account_info']
        return post_data

def get_sign(pdict):
        pstring = ''
        fields = ['tonce', 'accesskey', 'requestmethod', 'id', 'method', 'params']
        for f in fields:
                if pdict[f]:
                        if f == 'params':
                                param_string=str(pdict[f])
                                param_string=param_string.replace('None', '')
                                param_string=re.sub("[\[\] ]","",param_string)
                                param_string=re.sub("'",'',param_string)
                                pstring+=f+'='+param_string+'&'
                        else:
                                pstring+=f+'='+str(pdict[f])+'&'
                else:
                        pstring+=f+'=&'
        pstring=pstring.strip('&')
        phash = hmac.new(secret_key, pstring, hashlib.sha1).hexdigest()

        return base64.b64encode(access_key + ':' + phash)

class Namespace(BaseNamespace):

    def on_connect(self):
        print('[Connected]')

    def on_disconnect(self):
        print('[Disconnect]')

    def on_ticker(self, *args):
        print('ticker', args)

    def on_trade(self, *args):
        print('trade', args)

    def on_grouporder(self, *args):
        print('grouporder', args)

    def on_order(self, *args):
        print('order', args)

    def on_account_info(self, *args):
        print('account_info', args)

    def on_message(self, *args):
        print('message', args)

    def on_error(self, data):
        print(data)

socketIO = SocketIO('websocket.btcc.com', 80)
namespace = socketIO.define(Namespace)
namespace.emit('subscribe', 'marketdata_cnybtc')
namespace.emit('subscribe', 'marketdata_cnyltc')
namespace.emit('subscribe', 'marketdata_btcltc')
namespace.emit('subscribe', 'grouporder_cnybtc')
namespace.emit('subscribe', 'grouporder_cnyltc')
namespace.emit('subscribe', 'grouporder_btcltc')

payload = get_postdata()
arg = [json.dumps(payload), get_sign(payload)]
namespace.emit('private', arg)
socketIO.wait(seconds=2000000)
namespace.disconnect()

