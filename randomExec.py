"""
9-6로 1시간 마다 뽑기
"""
from datetime import datetime
import random

#resv_time=[(9,10),(10,10),(11,10),(12,10),(13,10),(14,10),(15,10),(16,10),(17,10),(18,10)]
resv_time=[(18,2),(18,3)]
visit = [0,0,0,0,0,0,0,0,0,0]
ind = 0
curr_hour, curr_min = 0,0
prev_hour=0
prev_min =0
res_hour , res_min = 0,0

def isTime():
    global ind
    curr_hour = datetime.today().hour
    curr_min = datetime.today().minute

    res_hour = resv_time[ind][0]
    res_min = resv_time[ind][1]
    global prev_hour,prev_min

    if (prev_hour == res_hour) and (prev_min == res_min):
        if (curr_hour!=res_hour) or (curr_min != res_min):
            ind+=1
    prev_hour, prev_min = curr_hour, curr_min

    if (curr_hour == res_hour) and (curr_min == res_min):
        if not visit[ind]:
            visit[ind]=1
            return True
    return False

i=0
while i<len(resv_time):
    if isTime():
        print("==========================================")
        print(resv_time[i])
        print(datetime.today().hour,datetime.today().minute)
        i+=1
        pass
    pass
