import socket, struct, pickle, cv2

import threading
import json, time
from datetime import date, datetime

ip = 'localhost'
port = 50001

def tcp_client(sock, addr):
  print('Connected by', addr)

  data_buffer = b""

  # calcsize : size of data(byte) - L : unsigned long  4 bytes
  data_size = struct.calcsize("L")

  while True:
    while len(data_buffer) < data_size:
      data_buffer += sock.recv(4096)

    packed_data_size = data_buffer[:data_size]
    data_buffer = data_buffer[data_size:] 
    
    # struct.unpack 
    # - >: big endian
    # - L: unsigned long 4 bytes 
    frame_size = struct.unpack(">L", packed_data_size)[0]
        
    while len(data_buffer) < frame_size:
      data_buffer += sock.recv(4096)

    frame_data = data_buffer[:frame_size]
    data_buffer = data_buffer[frame_size:]
    
    print("수신 프레임 크기 : {} bytes".format(frame_size))
    
    # loads: de-serialization
    frame = pickle.loads(frame_data)
    
    # imdecode : image decoding
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    
    # show frame
    cv2.imshow(f"Frame_{addr}", frame)
    
    # 'q' 키를 입력하면 종료
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
      break


  while True:
    try:
      data = sock.recv(65535)
      print('Received from', addr, data.decode())
      sock.sendall(data)

    except Exception as e:   
      print('exception has occured.', e)
      sock.close
      break

# create socket
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# bind 
server_socket.bind((ip, port))

# set listen clients count 
server_socket.listen(10) 

print('waiting clients.')


while True:
  sock, addr  = server_socket.accept()
  print('clients ip address:', addr[0])

  sock_th = threading.Thread(target=tcp_client, args=(sock, addr,))
  sock_th.start()


# closet socket
client_socket.close()
server_socket.close()
print('closed')

# close all windows
cv2.destroyAllWindows()
