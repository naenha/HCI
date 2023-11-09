import cv2
import pymysql
import datetime
from pathlib import Path

# connection 정보
conn = pymysql.connect(host = 'localhost', user = 'root', password = 'mysql', db = 'hci', charset = 'utf8')
curs = conn.cursor(pymysql.cursors.DictCursor)


# 모델 정보
BODY_PARTS = {"Neck": 1, "RShoulder": 2, "LShoulder": 5}
BASE_DIR = Path(__file__).resolve().parent
protoFile = str(BASE_DIR) + "/source/pose_deploy_linevec_faster_4_stages.prototxt"
weightsFile = str(BASE_DIR) + "/source/pose_iter_160000.caffemodel"
net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

# 카메라 정보
capture = cv2.VideoCapture(0)
inputWidth = 320;
inputHeight = 240;
inputScale = 1.0 / 255;

# 전역변수
cnt = 0  # 현재 추출 횟 수
N = 10  # 전체 추출 횟 수
scores = []  # 추출 점수
res = 0


# 함수
def extractNRL(frame, points):
    # 모델로 15 점 추출
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]
    inpBlob = cv2.dnn.blobFromImage(frame, inputScale, (inputWidth, inputHeight), (0, 0, 0), swapRB=False, crop=False)
    imgb = cv2.dnn.imagesFromBlob(inpBlob)
    net.setInput(inpBlob)
    output = net.forward()

    # NRL 정보 추출
    mat = [1, 2, 5]
    for j in range(3):
        i = mat[j]
        probMap = output[0, i, :, :]
        minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)
        x = (frameWidth * point[0]) / output.shape[3]
        y = (frameHeight * point[1]) / output.shape[2]

        # NRL 검출한 결과가 0.1보다 크면 points 추가, 아니면 None
        if prob > 0.1:
            points.append((int(x), int(y)))
        else:
            points.append(None)
    pass


def isTriangle(points):
    if points[0] and points[1] and points[2]: # 3점 다 찍힘
        if (points[1][0] < points[0][0]) and (points[0][0]<points[2][0]): # x좌표가 RNL 순
            if points[0][1] < min(points[1][1],points[2][1]): # y 좌표가 N이 작음
                return True
    return False


def isTime():
    return True

def score_turtle(frame,curs):
    global cnt
    points = []
    # NRL 추출
    extractNRL(frame, points)

    # points가 측정 가능한 삼각형을 이룸
    if isTriangle(points):
        x = abs(points[1][0] - points[2][0]) # 밑변
        h = abs(points[0][1] - (points[1][1] + points[2][1]) // 2) # 높이
        r = x // h # 비율
        cv2.putText(frame, "{0}".format((x,h,r)), (10,25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1,
                    lineType=cv2.LINE_AA)
        if r <= 3:
            scores.append(100)
            #cv2.line(frame, points[0], points[1], (255, 0, 0), 2)
            #cv2.line(frame, points[0], points[2], (255, 0, 0), 2)
        elif r <= 4:
            scores.append(80)
            #cv2.line(frame, points[0], points[1], (0, 255, 0), 2)
            #cv2.line(frame, points[0], points[2], (0, 255, 0), 2)
        elif r <= 5:
            scores.append(60)
            #cv2.line(frame, points[0], points[1], (0, 128, 127), 2)
            #cv2.line(frame, points[0], points[2], (0, 128, 127), 2)
        elif r <=6:
            scores.append(40)
            # cv2.line(frame, points[0], points[1], (0, 128, 127), 2)
            # cv2.line(frame, points[0], points[2], (0, 128, 127), 2)
        else:
            scores.append(20)
            #cv2.line(frame, points[0], points[1], (0, 0, 255), 2)
            #cv2.line(frame, points[0], points[2], (0, 0, 255), 2)
        cnt += 1
        pass

    # N번 추출함
    if cnt == N:
        global res
        res = sum(scores) // len(scores)
        # DB
        sql = """ insert into score(score, createdAt) values (%s, %s) """
        curs.execute(sql, (res, datetime.datetime.now()))
        conn.commit()

    pass


# 카메라 재생 , 아무 키나 누르면 끝난다.
while cv2.waitKey(1) < 0:

    hasFrame, frame = capture.read()

    if not hasFrame:
        cv2.waitKey()
        break

    """
    eyetracking 재생
    """

    # pose 추출 시간 발생
    if isTime():
        #pose 추출
        score_turtle(frame,curs)

    cv2.imshow("cam", frame)
    pass

# 카메라 종료
capture.release()
cv2.destroyAllWindows()

#print(scores)
print(res)