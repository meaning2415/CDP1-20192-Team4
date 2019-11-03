# a번째와 b번째 점 사이의 거리를 기준값(0에서 5번째점 사이의 거리)으로 나눈 것

import os
import numpy as np
from math import *

password_count=4 #비밀번호 개수
num_frame_count=5 #번호당 프레임 개수
testcase_count=3 #테스트케이스 개수
frame_element_count=14 #프레임 요소 개수


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

def calc_degree(hand):

    hand_key = [[0, 1, 2], [1, 2, 3], [2, 3, 4], [0, 5, 6], [5, 6, 7], [6, 7, 8], [0, 9, 10], [9, 10, 11], [10, 11, 12], [0, 13, 14], [14, 15, 16], [0, 17, 18], [17,18,19], [18, 19, 20]]
    result = []

    for a, std, b in hand_key:

        a = hand[a] - hand[std]
        b = hand[b] - hand[std]

        degree = degrees(acos((a[0] * b[0] + a[1] * b[1])/(sqrt(a[0] ** 2 + a[1] ** 2) * sqrt(b[0] ** 2 + b[1] ** 2))))

        result.append(degree)


    return(result)

def fread(flist):
    dataset=[]
    for fname in flist:
        f = open(fname)
        shape = []
        frame_mean=[]
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

            shape.append(calc_degree(np.array(hand)))

        shape=np.array(shape)
        for i in range(0,password_count*num_frame_count,num_frame_count):
            num_mean=[]
            temp = shape[i:i+num_frame_count]
            for j in range(0,frame_element_count):
                sum=0
                for frame in temp:
                    sum+=frame[j]
                num_mean.append(sum/num_frame_count)
            frame_mean.append(num_mean)
        dataset.append(frame_mean)
        f.close()
    return(dataset)

def make_std(dataset):
    std=[]
    for j in range(0,password_count):
        num_std_mean=[]
        for i in range(0,frame_element_count):
            sum=0
            for k in range(0,testcase_count):
                sum+=dataset[k][j][i]
            num_std_mean.append(sum/testcase_count)
        std.append(num_std_mean)
    return std

def compare_A(std,A):
    f = open(A)
    
    shape = []
    frame_mean=[]
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

        shape.append(calc_degree(np.array(hand)))

    shape=np.array(shape)
    for i in range(0,password_count*num_frame_count,num_frame_count):
        num_mean=[]
        temp = shape[i:i+num_frame_count]
        for j in range(0,frame_element_count):
            sum=0
            for frame in temp:
                sum+=frame[j]
            num_mean.append(sum/num_frame_count)
        frame_mean.append(num_mean)
    f.close()

    print(std)
    print(frame_mean)
    #여기서부터 비교
    count=0
    for i in range(0,password_count):
        for j in range(0,frame_element_count):
            if(abs(frame_mean[i][j]-std[i][j])<15):
                count+=1

    if(count>frame_element_count*password_count*0.8):
        return "OK"
    else:
        return "No!"


flist=["C:\\Users\\User\\Desktop\\analysis\\Data\\test1.txt","C:\\Users\\User\\Desktop\\analysis\\Data\\test2.txt","C:\\Users\\User\\Desktop\\analysis\\Data\\test3.txt"]
dataset=fread(flist)
std=make_std(dataset)
print(compare_A(std,"C:\\Users\\User\\Desktop\\analysis\\Data\\compare1.txt"))


#각도는 15
#비율은 0.1로 두면 구분됨 일단
