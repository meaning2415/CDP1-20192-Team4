from socket import *
from threading import Thread
import sys
import cv2
import os
from sys import platform
import argparse
import time
import re
import numpy

def make_rect(height, width):

        if(height > width):
            #right hand
            handRectangles = [
                [
                op.Rectangle(0., 0., 0., 0.),
                op.Rectangle(0., (height - width)/2, width, width)
                ]
            ]

        else:
            #right hand
            handRectangles = [
                [
                op.Rectangle(0., 0., 0., 0.),
                op.Rectangle((width - height)/2, 0., height, height)
                ]
            ]

        return handRectangles


def run_openpose(addr, data):

    #openpose dir
    dir_path="C:/Users/test/Desktop/openpose/build/examples/tutorial_api_python"

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = dir_path+"/../../../models/"
    params["hand"] = True
    params["hand_detector"] = 2
    params["body"] = 0

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()

    # Construct it from system arguments
    # op.init_argv(args[1])
    # oppython = op.OpenposePython()

    frame = data

    height, width, channels = frame.shape

    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    video = cv2.VideoWriter(str(addr) + ".avi", fourcc, 30.0, (width, height))
    out_file = open(str(addr) + ".txt", "a")

    #cv2.imshow("VideoFrame", frame)

    # Read image and face rectangle locations
    #imageToProcess = cv2.imread(args[0].image_path)

    # Create new datum
    datum = op.Datum()
    datum.cvInputData = frame
    datum.handRectangles = make_rect(height, width)

    # Process and display image
    opWrapper.emplaceAndPop([datum])

    out_file.write(str(datum.handKeypoints[1]))

    #cv2.imshow("OpenPose 1.5.1 - Tutorial Python API", datum.cvOutputData) #show image

    video.write(datum.cvOutputData)

    out_file.close()

    return datum.cvOutputData, datum.handKeypoints[1]


def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        
        buf += newbuf
        count -= len(newbuf)
    return buf




def data_receive(clientSock, addr):

    frame_size = clientSock.recv(30).decode()

    frame_size = int(frame_size, 2)

    print(frame_size)

    frame = 0

    while True:
        
        length = recvall(clientSock, 16)
        stringData = recvall(clientSock, int(length))
        data = numpy.fromstring(stringData, dtype = 'uint8')

        imageToProcess = cv2.imdecode(data, cv2.IMREAD_COLOR)

        print(int(length))
        print(str(frame) + "/" + str(frame_size))

        img_result, skeleton_result = run_openpose(addr, imageToProcess)
        print(img_result)
        #cv2.imshow('result', img_result)
        #cv2.waitKey(0)
        '''
        result_data = numpy.array(img_result)
        stringData = result_data.tostring()

        clientSock.sendall((str(len(stringData))).encode().ljust(16) + stringData)
        '''
        if(frame == frame_size):
            print('read end')
            break

        frame += 1
        clientSock.send('fend'.encode())
        print('send')


def run_server(host='127.0.0.1', port=8080):
    with socket(AF_INET, SOCK_STREAM) as serverSock:
        serverSock.bind(('', 8080))
        while True:
            serverSock.listen(5)
            clientSock, addr = serverSock.accept()
            # 새 연결이 생성되면 스레드를 만들어서 통신
            t = Thread(target=data_receive, args=(clientSock, addr))
            t.start()
        serverSock.close()



if __name__ == '__main__':

    # Import Openpose (Windows/Ubuntu/OSX)
    dir_path="C:/Users/test/Desktop/openpose/build/examples/tutorial_api_python"

    try:
        # Windows Import
        if platform == "win32":
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append(dir_path + '/../../python/openpose/Release');
            os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' +  dir_path + '/../../bin;'
            import pyopenpose as op
        else:
            # Change these variables to point to the correct folder (Release/x64 etc.)
            sys.path.append('../../python');
            # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
            # sys.path.append('/usr/local/python')
            from openpose import pyopenpose as op
    except ImportError as e:
        print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e

    run_server()
