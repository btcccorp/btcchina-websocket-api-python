""" An example for Python Socket.io Client
    Require installing socket.io client for Python first
    Refer to the source here to install socket.io client for Python: https://github.com/fuzeman/PySocketIO-Client
""" 

import pysocketio_client as io
import logging

#logging.basicConfig(level=logging.DEBUG)
socket = io.connect('https://websocket.btcchina.com')

@socket.on('connect')
def connected():
    print "connected"

socket.emit('subscribe', 'marketdata_cnybtc')
socket.emit('subscribe', 'marketdata_cnyltc')
socket.emit('subscribe', 'marketdata_btcltc')

@socket.on('trade')
def ticker(data):
    print "NEW Trade - %s" % data

while True:
    raw_input()
