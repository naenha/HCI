import cv2

ratio = 7
arr = [] # 순서 : 목xy, 왼어깨xy, 오른어깨 xy
        # 3번 반복 실행시 0 1 목 xy 2 3 왼어깨xy 45 오른어깨 xy
        # 67 목2 xy 89 왼어깨2 xy 1011 오른어깨 xy
        # 1213 목3xy 1415 왼어깨3 1617 오른어깨xy

def getCoor(arr):
    # MPII에서 각 파트 번호, 선으로 연결될 POSE_PAIRS
    # 1,2,5만 사용
    BODY_PARTS = {"Neck": 1, "RShoulder": 2, "LShoulder": 5}

    protoFile = "./pose_deploy_linevec_faster_4_stages.prototxt"
    weightsFile = "./pose_iter_160000.caffemodel"

    # 위의 path에 있는 network 모델 불러오기
    net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

    # 카메라 정보 받아옴
    capture = cv2.VideoCapture(0)
    inputWidth = 320;
    inputHeight = 240;
    inputScale = 1.0 / 255;

    # 반복문을 통해 카메라에서 프레임을 지속적으로 받아옴
    while True:  # 아무 키나 누르면 끝난다.
        # 웹캠으로부터 영상 가져옴
        hasFrame, frame = capture.read()

        # 웹캠으로부터 영상을 가져올 수 없으면 웹캠 중지
        if not hasFrame:
            # cv2.waitKey()
            break

        frameWidth = frame.shape[1]
        frameHeight = frame.shape[0]

        inpBlob = cv2.dnn.blobFromImage(frame, inputScale, (inputWidth, inputHeight), (0, 0, 0), swapRB=False,
                                        crop=False)
        imgb = cv2.dnn.imagesFromBlob(inpBlob)

        # network에 넣어주기
        net.setInput(inpBlob)

        # 결과 받아오기
        output = net.forward()

        # NRL 검출 이미지에 그려줌
        points = []
        mat = [1, 2, 5]
        for j in range(3):
            i = mat[j]
            # 해당 신체부위 신뢰도 얻음.
            probMap = output[0, i, :, :]

            # global 최대값 찾기
            minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

            # 원래 이미지에 맞게 점 위치 변경
            x = (frameWidth * point[0]) / output.shape[3]
            y = (frameHeight * point[1]) / output.shape[2]

            # 키포인트 검출한 결과가 0.1보다 크면(검출한곳이 위 BODY_PARTS랑 맞는 부위면) points에 추가, 검출했는데 부위가 없으면 None으로
            if prob > 0.1:
                cv2.circle(frame, (int(x), int(y)), 3, (0, 255, 255), thickness=-1,
                           lineType=cv2.FILLED)  # circle(그릴곳, 원의 중심, 반지름, 색)
                cv2.putText(frame, "x:{0},y:{1}".format(x, y), (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (0, 0, 255), 1,
                            lineType=cv2.LINE_AA)
                points.append((int(x), int(y)))
            else:
                points.append(None)

        # 길이 비율 계산
        # 7 이상이면 거북목
        if points[0] and points[1] and points[2]:

            arr.append(points[0][0])
            arr.append(points[0][1])
            arr.append(points[1][0])
            arr.append(points[1][1])
            arr.append(points[2][0])
            arr.append(points[2][1])

            if len(arr) % 6 == 0:
                print(arr)
                return arr
                capture.release()  # 카메라 장치에서 받아온 메모리 해제
                cv2.destroyAllWindows()  # 모든 윈도우 창 닫음
                break

            # # 밑변 길이 계산 (양 어깨의 x값 계산)
            # mit = abs(points[1][0]-points[2][0])
            # # 높이 계산 (neck의 y좌표 - 밑변의 y 좌표)
            # nop = abs(points[0][1]-int((points[1][1]+points[2][1])/2))
            # if nop == 0:
            #     bi = 100
            # else:
            #     bi = mit//nop
            #
            # curr=(mit,nop,bi) # 밑변, 높이, 비율
            #
            # if bi < ratio:
            #     print("정상 {0}".format(curr))
            #     cv2.line(frame, points[0], points[1], (0, 255, 0), 2)
            #     cv2.line(frame, points[0], points[2], (0, 255, 0), 2)
            #
            # else:
            #     print("거북복 {0}".format(curr))
            #     cv2.line(frame, points[0], points[1], (0, 0, 255), 2)
            #     cv2.line(frame, points[0], points[2], (0, 0, 255), 2)

        cv2.imshow("Output-Keypoints", frame)

    capture.release()  # 카메라 장치에서 받아온 메모리 해제
    cv2.destroyAllWindows()  # 모든 윈도우 창 닫음


def makeScore(arr):
    # 순서 : 목xy, 왼어깨xy, 오른어깨 xy
    # 3번 반복 실행시
    # 01 목 xy 23 왼어깨xy 45 오른어깨 xy
    # 67 목2 xy 89 왼어깨2 xy 1011 오른어깨 xy
    # 1213 목3xy 1415 왼어깨3 1617 오른어깨xy
    x1 = abs(arr[4]-arr[2])
    h1 = abs(arr[1] - int((arr[3]+arr[5])/2))
    r1 = x1 // h1

    x2 = abs(arr[4+6] - arr[2+6])
    h2 = abs(arr[1+6] - int((arr[3+6] + arr[5+6]) / 2))
    r2 = x2 // h2

    x3 = abs(arr[4 + 12] - arr[2 + 12])
    h3 = abs(arr[1 + 12] - int((arr[3 + 12] + arr[5 + 12]) / 2))
    r3 = x3 // h3

    r = (r1+r2+r3) / 3

    return r

getCoor(arr)
getCoor(arr)
getCoor(arr)
r = makeScore(arr)
print(r)


