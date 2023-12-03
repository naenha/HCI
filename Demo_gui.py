import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
import subprocess

# 시연용 GUI
class CustomWidget(QWidget):
    def __init__(self):
        super().__init__()

        CustomWidgetResult.capture = cv2.VideoCapture(0)
        CustomWidgetResult.cv2 = cv2

        # 박스의 색상 및 파일 매핑
        self.box_colors = [(255, 255, 0), (255, 182, 193)]
        self.file_paths = ['eye.py']

        # 박스를 클릭할 때 실행할 함수 연결
        self.box_click_handlers = [self.open_eye, self.open_posture]

        # 결과 창을 저장할 변수 추가
        self.result_widget = None

        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Main')

        # 박스를 표시할 QLabel들을 만듭니다.
        self.labels = [QLabel(self) for _ in range(2)]

        # 박스의 배경색 및 텍스트 설정
        for i, label in enumerate(self.labels):
            color = QColor(*self.box_colors[i])
            label.setAutoFillBackground(True)
            label.setStyleSheet(f"QLabel {{ background-color: {color.name()}; }}")
            label.setAlignment(Qt.AlignCenter)
            labels_text = ['눈', '자세']
            label.setText(labels_text[i])
            label.mousePressEvent = lambda event, idx=i: self.on_box_click(idx)

        # QVBoxLayout을 사용하여 박스들을 수직으로 배치합니다.
        layout = QVBoxLayout(self)
        for label in self.labels:
            layout.addWidget(label)

        # Add information button
        info_button = QPushButton('프로그램 사용법', self)
        info_button.setToolTip('Click for information')
        info_button.clicked.connect(self.show_information)
        layout.addWidget(info_button)

        self.show()

    def on_box_click(self, idx):
        # 박스를 클릭했을 때 실행할 함수 호출
        self.box_click_handlers[idx]()

    def show_information(self):
        # Show information in a QMessageBox
        info_message = ("눈 버튼을 누르면 피곤할 때 미로가 실행되며 눈 운동을 할 수 있습니다.\n\n"
                        "자세를 기록하려면 처음 혹은 모니터 위치가 바뀔 때 좋은 자세와 안 좋은 자세 사진을 찍어주세요.\n\n"
                        "좋은 자세, 안 좋은 자세 사진을 기준으로 현 자세의 점수가 매겨집니다.\n\n "
                        "달력을 누르면 그간의 점수를 확인하실 수 있습니다.\n\n "
                        "그간의 내 자세를 돌아보고 앞으로의 자세를 개선해보세요!")
        QMessageBox.information(self, 'Information', info_message)

    def open_eye(self):
        subprocess.Popen(['python', self.file_paths[0]])

    def open_posture(self):
        # 결과 창이 이미 열려 있으면 숨기기/보이기 토글
        if self.result_widget is not None:
            if self.result_widget.isVisible():
                self.result_widget.hide()
            else:
                self.result_widget.show()
        else:
            # 결과 창이 열려 있지 않으면 생성하고 보이기
            print("Opening posture result window.")
            self.result_widget = CustomWidgetResult()
            self.result_widget.show()

class CustomWidgetResult(QWidget):
    capture = None
    cv2 = None

    def __init__(self):
        super().__init__()
        self.box_colors = [(173, 216, 230), (173, 216, 230),(173, 216, 230)]
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Main ')

        # 박스를 표시할 QLabel들을 만듭니다.
        self.labels = [QLabel(self) for _ in range(3)]
        self.file_paths = ['extract_std.py','final_main.py','calendar.py']

        # 박스를 클릭할 때 실행할 함수 연결
        self.box_click_handlers = [self.open_ref, self.open_posture, self.open_result]

        # 박스의 배경색 및 텍스트 설정
        for i, label in enumerate(self.labels):
            color = QColor(*self.box_colors[i])
            label.setAutoFillBackground(True)
            label.setStyleSheet(f"QLabel {{ background-color: {color.name()}; }}")
            label.setAlignment(Qt.AlignCenter)
            labels_text = ['기준 촬영', '실행','달력']
            label.setText(labels_text[i])
            label.mousePressEvent = lambda event, idx=i: self.on_box_click(idx)

        # QVBoxLayout을 사용하여 박스들을 수직으로 배치합니다.
        layout = QVBoxLayout(self)
        for label in self.labels:
            layout.addWidget(label)

    def on_box_click(self, idx):
        # 박스를 클릭했을 때 실행할 함수 호출
        self.box_click_handlers[idx]()

    def open_ref(self):
        if CustomWidgetResult.capture is not None and CustomWidgetResult.cv2 is not None:
            process = subprocess.Popen(['python', self.file_paths[0]])
            process.communicate()  # Wait for the subprocess to complete
            CustomWidgetResult.capture.release()
            CustomWidgetResult.cv2.destroyAllWindows()

    def open_posture(self):
        subprocess.Popen(['python', self.file_paths[1]])

    def open_result(self):
        # print("Opening file:", self.file_paths[1])
        subprocess.Popen(['python', self.file_paths[2]])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = CustomWidget()
    sys.exit(app.exec_())
