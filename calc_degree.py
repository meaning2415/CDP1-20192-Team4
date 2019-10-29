import os
import numpy as np
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

fname = "C:\\Users\\test\\Desktop\\새 폴더 (2)\\analysis\\KakaoTalk_Video_20191021_0914_36_790.mp4.txt"
f = open(fname)

while True:
    line = f.readline()
    if not line: break
    print(line)
    hand = []
    for i in range(0, 21):
        line = f.readline()[3:-1]
        line = line.replace(']', '')
        line = line.split(' ')

        for j in range(0,3):
            line[j] = float(line[j])
        hand.append(line)

    calc_degree(np.array(hand))


f.close()
