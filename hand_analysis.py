import os
import numpy as np
from math import *

FRAME_CNT = 5
PWD_CNT = 4

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


    return result

def calc_pos(hand):

    std = hand[0]
    hand = np.array(hand) - std

    return hand

def fread(flist):
    dataset=[]
    for fname in flist:
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

            shape.append(np.array(hand))
        dataset.append(shape)
        f.close()
    print(len(dataset))
    return dataset

def mean_degree(dataset):

    result = []
    #값을 degree 정보로 바꿈
    for i in range(0, len(dataset)):
        for j in range(0, len(dataset[i])):
            dataset[i][j] = calc_degree(dataset[i][j])

    for shape in dataset:
        shape = np.array(shape)
        #입력 데이터셋 평균값 구하기
        num_mean=[]
        for i in range(0, PWD_CNT*FRAME_CNT, FRAME_CNT):

            total = np.array(shape[i])
            for temp in shape[i+1:i+FRAME_CNT]:
                total += np.array(temp)

            num_mean.append(list(total/FRAME_CNT))

        result.append(np.array(num_mean))

    #데이터셋에서 추출해낸 유저구분 기준

    result = sum(result)/len(result)

    return result

def mean_pos(dataset):
    result = []
    #값을 degree 정보로 바꿈
    for i in range(0, len(dataset)):
        for j in range(0, len(dataset[i])):
            dataset[i][j] = calc_pos(dataset[i][j])

    for shape in dataset:
        shape = np.array(shape)
        #입력 데이터셋 평균값 구하기
        num_mean=[]
        for i in range(0, PWD_CNT*FRAME_CNT, FRAME_CNT):

            total = np.array(shape[i])
            for temp in shape[i+1:i+FRAME_CNT]:
                total += np.array(temp)

            num_mean.append(list(total/FRAME_CNT))

        result.append(np.array(num_mean))

    #데이터셋에서 추출해낸 유저구분 기준
    result = sum(result)/len(result)

    return result

def mean_ratio(dataset):
    result = []
    #값을 degree 정보로 바꿈
    for i in range(0, len(dataset)):
        for j in range(0, len(dataset[i])):
            dataset[i][j] = calc_ratio(dataset[i][j])

    for shape in dataset:
        shape = np.array(shape)
        #입력 데이터셋 평균값 구하기
        num_mean=[]
        for i in range(0, PWD_CNT*FRAME_CNT, FRAME_CNT):

            total = np.array(shape[i])
            for temp in shape[i+1:i+FRAME_CNT]:
                total += np.array(temp)

            num_mean.append(list(total/FRAME_CNT))

        result.append(np.array(num_mean))

    #데이터셋에서 추출해낸 유저구분 기준

    result = sum(result)/len(result)

    return result

def compare_A(std,A, STD_CONST):

    count = 0
    for pwd in abs(A - std):
        for i in pwd:
            if i < STD_CONST:
                #print("valid")
                count += 1

    if(count>FRAME_CNT * PWD_CNT * 0.8):
        return True
    else:
        return False

def compare_pos(std,A, STD_CONST):

    count = 0
    for pwd in abs(A - std):
        for i in pwd:
            length = sqrt(i[0]**2 + i[1] ** 2)
            if length < STD_CONST:
                #print("valid")
                count += 1

    if(count>FRAME_CNT * PWD_CNT * 0.8):
        return True
    else:
        return False


flist=["test1.txt","test2.txt","test3.txt"]
dataset = fread(flist)
print(len(dataset[1]))
result = mean_ratio(dataset)

std = open("std.txt", "w")
A = open("A.txt", "w")

dataset_A = fread(["compare1.txt"])
result_a = mean_ratio(dataset_A)

stdW = str(result).replace("[", "").replace("\n", "").replace("]", "\n")
std.write(stdW)
AW = str(result_a).replace("[", "").replace("\n", "").replace("]", "\n")
A.write(AW)

std.close()
A.close()

print(compare_A(result, result_a, 0.1))

#좌표 비교
'''
flist=["test1.txt","test2.txt","test3.txt"]
dataset = fread(flist)
result = mean_pos(dataset)

dataset_A = fread(["compare1.txt"])
result_a = mean_pos(dataset_A)

print(compare_pos(result, result_a, 15))
'''

#각도 비교
'''
flist=["test1.txt","test2.txt","test3.txt"]
dataset = fread(flist)
result = mean_degree(dataset)

dataset_A = fread(["compare1.txt"])
result_a = mean_degree(dataset_A)

print(compare_A(result, result_a, 15))
'''

#비율 비교
'''
flist=["test1.txt","test2.txt","test3.txt"]
dataset = fread(flist)
result = mean_ratio(dataset)

dataset_A = fread(["compare1.txt"])
result_a = mean_ratio(dataset_A)

print(compare_A(result, result_a, 0.1))
'''

#print(compare_A(result, result_a))
