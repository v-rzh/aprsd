#!/usr/bin/python

# example incoming message:
# KM6LYW>APRS,TCPIP*,qAC,FOURTH::KM6LYW-4 :test message to telnet
# KM6LYW-4>APRS,TCPIP*,qAC,T2TEXAS::KM6LYW-9 :This is a test message
#
# from radio:
# KM6LYW>APY01D,PINE*,WIDE2-1,qAR,KJ6NKR-2::KM6LYW-9 :time please{15

import sys
import telnetlib
import time
import re

HOST = "texas.aprs2.net"
USER = "KM6LYW-9"
PASS = "11111"

def send_ack(tocall, ack):
  print "Sending ack __________________"
  print "To         : " + tocall
  print "Ack number : " + ack
  tn.write("KM6LYW-9>APRS,TCPIP*::" + tocall + ":ack" + ack + "\n")

def send_message(tocall, message):
  print "Sending message_______________"
  print "To         : " + tocall
  print "Message    : " + message
  tocall = tocall.ljust(9) # pad to nine chars
  tn.write("KM6LYW-9>APRS,TCPIP*::" + tocall + ":" + message + "\n")
### end send_ack()

def process_message(line):
  f = re.search('(.*)>', line)
  fromcall = f.group(1)
  m = re.search('::KM6LYW-9 :(.*)', line)
  fullmessage = m.group(1)
  searchresult = re.search('(.*){(.*)', fullmessage)

  if searchresult:
    message= searchresult.group(1)
    ack = searchresult.group(2)
  else:
    message = fullmessage
    ack = "none"

  print "Received message______________"
  print "From       : " + fromcall
  print "Message    : " + message
  print "Ack number : " + ack

  send_ack(fromcall, ack)
  send_message(fromcall, "This is a reply.")
### end process_message()
  
tn = telnetlib.Telnet(HOST, 14580)

time.sleep(2)
tn.write("user " + USER + " pass " +  PASS + " vers aprsd 0.99\n" )

while True:
  line = ""
  for char in tn.read_until("\n",100):
    line = line + char 
  line = line.replace('\n', '')
  print line
  if re.search("::KM6LYW-9 ", line):
     process_message(line)
  
# end while True

tn.close()

exit()
