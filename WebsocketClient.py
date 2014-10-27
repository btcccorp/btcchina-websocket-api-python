""" An example for Python Socket.io Client
    Require installing socket.io client for Python first
    Refer to the source here to install socket.io client for Python: https://github.com/fuzeman/PySocketIO-Client
""" 

import pysocketio_client as io
import logging
import time
import json
import re
import hmac
import hashlib
import base64

access_key = "<YOUR ACCESS KEY>"
secret_key = "<YOUR SECRET KEY>"

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
                                param_string=str(pdict[f]);
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
        
#logging.basicConfig(level=logging.DEBUG)
socket = io.connect('https://websocket.btcchina.com')

@socket.on('connect')
def connected():
    print "Connected!"

socket.emit('subscribe', 'marketdata_cnybtc')
socket.emit('subscribe', 'marketdata_cnyltc')
socket.emit('subscribe', 'marketdata_btcltc')
socket.emit('subscribe', 'grouporder_cnybtc')
socket.emit('subscribe', 'grouporder_cnyltc')
socket.emit('subscribe', 'grouporder_btcltc')

payload = get_postdata()
arg = [json.dumps(payload), get_sign(payload)]
socket.emit('private', arg)

@socket.on('message')
def message(data):
    print "New Message - %s" % data
    
@socket.on('trade')
def trade(data):
    print "New Trade - %s" % data

@socket.on('ticker')
def ticker(data):
    print "New Ticker - %s" % data

@socket.on('grouporder')
def grouporder(data):
    print "New GroupOrder - %s" % data

@socket.on('order')
def order(data):
    print "New Order - %s" % data
    
@socket.on('account_info')
def account_info(data):
    print "New Account_info - %s" % data    

while True:
    raw_input()
