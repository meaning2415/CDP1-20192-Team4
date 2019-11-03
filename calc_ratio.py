# a번째와 b번째 점 사이의 거리를 기준값(0에서 5번째점 사이의 거리)으로 나눈 것

import os
import numpy as np
from math import *

def calc_ratio(hand):

    hand_key = [[0,1],[1,2],[2,3],[3,4],[0,5],[5,6],[6,7],[7,8],[0,9],[9,10],[10,11],[11,12],[0,13],[13,14],[14,15],[15,16],[0,17],[17,18],[18,19],[19,20]]
    result = []

    hand_std=hand[5]-hand[0]
    hand_std_length=sqrt(hand_std[0]**2+hand_std[1]**2)

    for a, b in hand_key:

        distance_a_to_b=hand[b]-hand[a]
        distance_a_to_b_length=sqrt(distance_a_to_b[0]**2+distance_a_to_b[1]**2)
        ratio=distance_a_to_b_length/hand_std_length
        
        result.append(ratio)


    return(result)

def fread(fname):
    f = open(fname)
    shape = []
    while True:
        line = f.readline()
        if not line: break
        hand = []
        for i in range(0, 21):
            line = f.readline()[3:-1]
            line = line.replace(']', '')
            line = line.split(' ')

            for j in range(0,3):
                line[j] = float(line[j])
            hand.append(line)

        shape.append(calc_ratio(np.array(hand)))
    f.close()

    shape = np.array(shape)
    num = shape[0]
    for i in shape:
        print(i)

fname="C:\\Users\\User\\Desktop\\analysis\\KakaoTalk_Video_20191021_0914_33_134.mp4\\KakaoTalk_Video_20191021_0914_33_134.mp4.txt"
fread(fname)
