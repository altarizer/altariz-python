import socket
import time
from datetime import datetime

MCAST_GRP = '234.234.234.234' #'224.1.1.1'
MCAST_PORT = 5004
MCAST_TTL = 2 # 2-hop restriction in network

class sender:
  
  def __init__(self, mc_group=MCAST_GRP, mc_port=MCAST_PORT, mc_ttl=MCAST_TTL):

    self.mc_group = mc_group
    self.mc_port = mc_port
    self.mc_ttl = mc_ttl

    self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, self.mc_ttl)

  def send(self, data=""):
    nb = bytes(data, "utf-8")
    self.sock.sendto(nb, (self.mc_group, self.mc_port))

  def close(self):
    self.sock.close()
