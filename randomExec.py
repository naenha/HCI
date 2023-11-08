"""
예약 시간에 한번 추출 했으면 예약시간이어도 넘어감 => 중복 방지
추출 실패 대비해서 여러개 설정
대안1. 그냥 사용자가 처음에 예측 사용 시간 설정해 놓고 균일 한 시간에 촬영 ...
"""

from datetime import datetime
import random


resv_time=[]
visit = []
cnt = 0
N = 4
def randTime():

    pass
def isTime():
    global cnt
    curr_hour = datetime.today().hour  
    curr_min = datetime.today().minute
    if (curr_hour==resv_time[cnt][0]) and (curr_min==resv_time[cnt][1]+1):
        cnt+=1

    res_hour = resv_time[cnt][0]
    res_min = resv_time[cnt][1]
    if (curr_hour == res_hour) and (curr_min == res_min):
        if not visit[cnt]:
            visit[cnt]=1
            return True
    return False


check=0
while True:
    if isTime():
        pass
    pass
