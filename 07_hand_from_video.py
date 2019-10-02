# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse
import time
import re

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

# Import Openpose (Windows/Ubuntu/OSX)
dir_path = os.path.dirname(os.path.realpath(__file__))
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
parser.add_argument("--image_path", default="../../../examples/media/hand_detect.mp4", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
args = parser.parse_known_args()

# Custom Params (refer to include/openpose/flags.hpp for more parameters)
params = dict()
params["model_folder"] = "../../../models/"
params["hand"] = True
params["hand_detector"] = 2
params["body"] = 0

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

capture = cv2.VideoCapture(args[0].image_path)
fourcc = cv2.VideoWriter_fourcc(*'XVID')

ret, frame = capture.read()

height, width, channels = frame.shape

video = cv2.VideoWriter("output.avi", fourcc, 30.0, (width, height))
out_file = open("output.txt", "w")
try:
    while capture.isOpened():


        ret, frame = capture.read()

        if ret:
            #cv2.imshow("VideoFrame", frame)

            # Read image and face rectangle locations
            #imageToProcess = cv2.imread(args[0].image_path)

            # Create new datum
            datum = op.Datum()
            datum.cvInputData = frame
            print(height,width)
            datum.handRectangles = make_rect(height, width)

            # Process and display image
            opWrapper.emplaceAndPop([datum])
            print("Right hand keypoints: \n" + str(datum.handKeypoints[1]))
            out_file.write(str(datum.handKeypoints[1]))
            #cv2.imshow("OpenPose 1.5.1 - Tutorial Python API", datum.cvOutputData)

            video.write(datum.cvOutputData)


        else:
            break

    out_file.close()
    capture.release()
    output.release()
    cv2.destroyAllWindows()

except Exception as e:
    print(e)
    sys.exit(-1)
