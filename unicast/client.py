import cv2 
import socket, pickle, struct 
import time

ip = 'localhost'
port = 50001

# cam or movies
capture = cv2.VideoCapture(0)

# set frame size
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) # 가로
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) # 세로

# create socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
  # connect
  client_socket.connect((ip, port))
  
  print("connected")
  
  # recv
  while True:
    time.sleep(1/15)
    # read frames
    retval, frame = capture.read()
    
    # imencode : encode image(frame)
    # params
    # - jpg / cv2.IMWRITE_JPEG_QUALITY / 0 ~ 100
    #   png / cv2.IMWRITE_PNG_COMPRESSION / 0 ~ 9
    # return
    # - result / (True / False)
    # - encoded image
    retval, frame = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
    
    # dumps : serialization
    frame = pickle.dumps(frame)

    print("sent frame size : {} bytes".format(len(frame)))
    
    # sendall : send datas
    # struct.pack : big endian
    # - L : unsigned long 4 bytes
    client_socket.sendall(struct.pack(">L", len(frame)) + frame)


# release
capture.release()
