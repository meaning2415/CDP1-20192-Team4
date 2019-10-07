from socket import *
import os
import cv2
import numpy

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf


address = 'localhost'
port = 8080

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect((address, port))

filename = './hand2.mp4'

capture = cv2.VideoCapture(filename)
total_frame = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
print(total_frame)
clientSock.send(bin(total_frame).encode())

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    if(capture.get(cv2.CAP_PROP_POS_FRAMES) == capture.get(cv2.CAP_PROP_FRAME_COUNT)):
        capture.open(filename)

    ret, frame = capture.read()
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    
    data = numpy.array(frame)
    stringData = data.tostring()
    print(len(stringData))

    #String 형태로 변환한 이미지를 socket을 통해서 전송
    clientSock.sendall((str(len(stringData))).encode().ljust(16) + stringData)
    
    flag = clientSock.recv(4)
    '''
    stringData = recvall(clientSock, int(length))
    data = numpy.fromstring(stringData, dtype = 'float')

    imageToProcess = cv2.imdecode(data, cv2.IMREAD_COLOR)
    cv2.imshow('result', imageToProcess)
    '''
    print(flag.decode())
    
    
    
    
            

capture.release()
cv2.destroyAllWindows()
clientSock.close()

'''
data_transferred = 0;
clientSock.send(filename.encode('utf-8'))

#send total file size
total_file_size = os.stat(filename).st_size
print(bin(total_file_size).encode())

clientSock.send(bin(total_file_size).encode())


with open(filename,'rb') as f:
    try:
        data = f.read(1024) # 파일을 1024바이트 읽음
        while data: # 파일이 빈 문자열일때까지 반복
            data_transferred += clientSock.send(data)
            data = f.read(1024)
            
            print(str(data_transferred) + '/' + str(total_file_size))
    except Exception as e:
        print(e)

print(clientSock.recv(1024).decode())
clientSock.close()
'''



