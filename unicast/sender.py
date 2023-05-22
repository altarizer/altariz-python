import cv2 
import socket, pickle, struct 
import time
import numpy as np

UCAST_IP = 'localhost' 
UCAST_PORT = 50001

class sender:
  
  def __init__(self, ucast_ip=UCAST_IP, ucast_port=UCAST_PORT):

    self.ucast_ip = ucast_ip
    self.ucast_port = ucast_port

    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.connect((ucast_ip, ucast_port))
    print("connected")

  def send(self, frame, id=0):
    retval, frame = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
    
    # dumps : serialization
    
    # mix id in stream
    # print (frame)
    hexid = f'{id:x}'
    #print(hexid)
    #_hexid = hexId[2:]
    #print (_hexid)
    #print (len(hexid) % 2)
    if len(hexid) < 6:
      hexid = hexid.zfill(6) 
    #print (hexid)
    hexas = [hexid[i:i+2] for i in range(0, len(hexid), 2)]
    #print (hexas)

    frame[-3:]= np.array([[int(hexas[-3], 16), int(hexas[-2], 16), int(hexas[-1], 16) ]]).astype(np.uint32)
    #print(frame)

 
    frame = pickle.dumps(frame)
    #print("sent frame size : {} bytes".format(len(frame)))
        
    # sendall : send datas
    # struct.pack : big endian
    # - L : unsigned long 4 bytes
    self.sock.sendall(struct.pack(">L", len(frame)) + frame)

  def close(self):
    self.sock.close()

