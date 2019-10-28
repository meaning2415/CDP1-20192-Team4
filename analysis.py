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
from math import *

def calc_degree(hand):

    hand_key = [[0, 1, 2], [1, 2, 3], [2,3,4], [0, 5, 6], [5, 6, 7], [6, 7, 8], [0, 9, 10], [9, 10, 11], [10, 11, 12], [0, 13, 14], [14, 15, 16], [0, 17, 18], [17,18,19], [18, 19, 20]]
    result = []

    for a, std, b in hand_key:

        a = hand[a] - hand[std]
        b = hand[b] - hand[std]

        degree = degrees(acos((a[0] * b[0] + a[1] * b[1])/(sqrt(a[0] ** 2 + a[1] ** 2) * sqrt(b[0] ** 2 + b[1] ** 2))))

        result.append(degree)


    print(result)

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


def run_openpose(opWrapper, path, fname):


    capture = cv2.VideoCapture(path)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    ret, frame = capture.read()

    height, width, channels = frame.shape

    out_file = open(fname + "/" + fname+".txt", "w")
    video = cv2.VideoWriter(fname + "/" + fname + ".avi", fourcc, 30.0, (width, height))
    total_frame = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_count = 0

    while capture.isOpened():

        ret, frame = capture.read()

        if ret:
            #cv2.imshow("VideoFrame", frame)

            # Read image and face rectangle locations
            #imageToProcess = cv2.imread(args[0].image_path)

            # Create new datum
            datum = op.Datum()
            datum.cvInputData = frame
            datum.handRectangles = make_rect(height, width)

            # Process and display image
            opWrapper.emplaceAndPop([datum])

            print(str(frame_count) + "/" + str(total_frame) + str(datum.handKeypoints[1]))

            calc_degree(datum.handKeypoints[1][0])

            out_file.write(str(frame_count) + '\n')
            out_file.write(str(datum.handKeypoints[1]) + '\n')

            #cv2.imshow("OpenPose 1.5.1 - Tutorial Python API", datum.cvOutputData) #show image

            cv2.imwrite(fname + "/" + fname + "_" + str(frame_count) + ".jpg", datum.cvOutputData)
            video.write(datum.cvOutputData)
            frame_count+=1


        else:
            break

    out_file.close()
    capture.release()


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

    # Flags
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_path", default="./input", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
    args = parser.parse_known_args()

    # Custom Params (refer to include/openpose/flags.hpp for more parameters)
    params = dict()
    params["model_folder"] = dir_path+"/../../../models/"
    params["hand"] = True
    params["hand_detector"] = 2
    params["body"] = 0
    print(params)
    # Add others in path?
    for i in range(0, len(args[1])):
        curr_item = args[1][i]
        if i != len(args[1])-1: next_item = args[1][i+1]
        else: next_item = "1"
        if "--" in curr_item and "--" in next_item:
            key = curr_item.replace('-','')
            if key not in params:  params[key] = "1"
        elif "--" in curr_item and "--" not in next_item:
            key = curr_item.replace('-','')
            if key not in params: params[key] = next_item

    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()
    # Construct it from system arguments
    # op.init_argv(args[1])
    # oppython = op.OpenposePython()

    path = "./input"
    file_list = os.listdir(path)

    for name in file_list:
        print(name)
        if not(os.path.isdir(name)):
            os.makedirs(os.path.join(name))
        run_openpose(opWrapper, path+'/'+name, name)
