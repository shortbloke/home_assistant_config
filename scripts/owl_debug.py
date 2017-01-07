#!/usr/bin/env python
# Original Source: https://openenergymonitor.org/emon/node/11109
# Network OWL pages:
#  - Information: https://theowl.zendesk.com/hc/en-gb/articles/201284603-Multicast-UDP-API-Information
#  - Network OWL Multicast: https://theowl.zendesk.com/hc/en-gb/article_attachments/200344663/Network_OWL_Multicast.pdf
#  - Network OWL Public API: https://theowl.zendesk.com/hc/en-gb/article_attachments/200501167/Network_OWL_API__Public_.pdf
# Modified by Martin Rowan, 2017
# Requires: sudo install xmltodict

import socket
import struct
import xmltodict
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
# create console handler and set level to debug
ch = logging.StreamHandler()
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)
OWL_DEVICE_ID = '443719100B48'

MCAST_GRP = '224.192.32.19'
MCAST_PORT = 22600

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))  # use MCAST_GRP instead of '' to listen only
                             # to MCAST_GRP, not all groups on MCAST_PORT
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
  logger.info("OWL Multicast Packet Received")
  raw = sock.recv(1024)
  logger.debug(raw)
  data = xmltodict.parse(raw)
  logger.debug(data)
  if 'electricity' in data:
    logger.debug("Packet containts electricty payload")
    if data['electricity']['@id'] == OWL_DEVICE_ID:
      logger.debug("Found matching ID for Electricty")
      print "rssi       : " + data['electricity']['signal']['@rssi']
      print "lqi        : " + data['electricity']['signal']['@lqi']
      print "batt level : " + data['electricity']['battery']['@level'][:-1]\
        + " " + data['electricity']['battery']['@level'][-1]
      for ct in (0, 1, 2):
        if data['electricity']['channels']['chan'][ct]:
          print "CT" + str(ct + 1) + " power  : " \
            + data['electricity']['channels']['chan'][ct]['curr']['#text'] + " " \
            + data['electricity']['channels']['chan'][ct]['curr']['@units']
          print "CT" + str(ct + 1) + " energy : " \
            + data['electricity']['channels']['chan'][ct]['day']['#text'] + " " \
            + data['electricity']['channels']['chan'][ct]['day']['@units']
  elif 'solar' in data:
    logger.debug("Packet containts Solar payload")
    if data['solar']['@id'] == OWL_DEVICE_ID:
      logger.debug("Found matching ID for Solar")
      print "generating : " + data['solar']['current']['generating']['#text']\
        + " " + data['solar']['current']['generating']['@units']
      print "generated  : " + data['solar']['day']['generated']['#text']\
        + " " + data['solar']['day']['generated']['@units']
      print "exporting  : " + data['solar']['current']['exporting']['#text']\
        + " " + data['solar']['current']['exporting']['@units']
      print "exported   : " + data['solar']['day']['exported']['#text']\
        + " " + data['solar']['day']['exported']['@units']
  else:
    if 'weather' in data:
      logger.warning('Weather - Not implemented')
    elif 'heating' in data:
      loger.warning('Heating -  Not implemented')
    elif 'hot_water' in data:
      logger.warning('Hot_Water - Not implemented')
    elif 'relays' in data:
      logger.warning('Relays - Not implemented')
    else:
      logger.info("Unexpected packet: " + data)
