
import threading
import socket, struct

from colorama import Fore as fore, Style as style, init
init(convert=True)

MCAST_GRP = '234.234.234.234' #'224.1.1.1'
MCAST_PORT = 5004

def mcast_recv(args): 

  sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  sock.bind(('', MCAST_PORT))
  mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
  sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

  while True:
    print(sock.recv(65535))

# daemon thread
th = threading.Thread(target=mcast_recv, args=('nth',))
th.daemon = True 
th.start()


print(f"{style.BRIGHT}{fore.YELLOW}Press any key to quit.{style.RESET_ALL}")
input()
