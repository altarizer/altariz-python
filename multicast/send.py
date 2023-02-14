import socket
import time
from datetime import datetime


MCAST_GRP = '234.234.234.234' #'224.1.1.1'
MCAST_PORT = 5004
# 2-hop restriction in network
ttl = 2
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

#data = B'11'
# bytes("{} hello world".format(time.time()), "utf-8")

while True:
  time.sleep(0.1)

  strDt = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
  data = bytes("[{}] hello world".format(strDt), "utf-8")
  sock.sendto(data, (MCAST_GRP, MCAST_PORT))
