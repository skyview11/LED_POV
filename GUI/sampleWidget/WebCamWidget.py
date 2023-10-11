import cv2
from threading import Thread
import sys
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout
import numpy as np
from PyQt5.QtCore import pyqtSignal, QObject
from time import sleep

# on 신호가 오면 카메라 키고, off 신호 오면 끄는 위젯
class WebCamWidget(QWidget):
    def __init__(self, test = False):
        super().__init__()
        # 초기 변수(나중에 argparse로 이동 예정)
        
        self.test = test # 이 파일이 main인 경우에만 활성화
        self.mirror = True # 카메라 거울모드 여부
        self.mirror = 1 if self.mirror else 0
        
        # 전원변수(?)
        self.camon = False
        self.running = False
        self.r = 100
        
        self.communicator = Communicate()
        
        self.init_ui() 
        
    def init_ui(self, filter = None):
        # 카메라 표시하는 레이블 생성
        self.title = QLabel("WebCam")
        self.image = QLabel() # 나중에 run 함수에서 pixmap을 mapping 해 줄 예정
        self.infobar = QLabel("INFO BAR")
        
        # test 모드에서만 추가되는 위젯(camon, camoff 버튼)
        if self.test:
            self.btn_start = QPushButton("Cam On")
            self.btn_stop = QPushButton("Cam Off")
            self.btn_start.clicked.connect(self.start)
            self.btn_stop.clicked.connect(self.stop)
        
        # 레이아웃 생성 및 위젝 추가
        layout = QGridLayout()
        layout.addWidget(self.title, 0, 0)
        layout.addWidget(self.image, 1, 0)
        layout.addWidget(self.infobar, 2, 0)
        if self.test:
            layout.addWidget(self.btn_start, 3, 0)
            layout.addWidget(self.btn_stop , 3, 1)           
        
        # 위젯에 레이아웃 설정
        self.setLayout(layout)
    
    def run(self): # 이미지 캡쳐 -> 형태변환 -> self.image에 assign
        # 이미지 캡쳐
        cap = cv2.VideoCapture(0)
        self.w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(self.w, self.h)
        self.image.resize(self.w, self.h)
        while self.running:
            ret, img = cap.read()

            if ret:
                # 형태 변환
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.flip(img, self.mirror)
                h,w,c = img.shape
                cv2.circle(img, (w//2,h//2), self.r, (0,0,255))
                qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(qImg)
                
                # aasign
                self.image.setPixmap(pixmap)   
                self.communicator.data_passed.emit(Img2Conv(img, (w//2, h//2), self.r)) 
            else:
                QtWidgets.QMessageBox.about(self, "Error", "Cannot read frame.")
                print("cannot read frame.")
                break                
        cap.release()
        print("Thread end. ")
           
    def readCamAtive(self, isOn): # 밖에서 이 함수를 호출해 카메라 조정을 한다. 
        if isOn:
            self.start()
        else:
            self.stop()
    
    def stop(self):
        self.running = False
        print("stoped..")
    
    def start(self):
        self.running = True
        th = Thread(target=self.run)
        th.start()
        print("started.. ")
        
    def onExit(self):
        print("EXIT")
        self.stop()
    def getImgInfo(self):
        return self.imgout
class Img2Conv():
    def __init__(self, image, center, radius):
        self.image = image
        self.center = center
        self.radius = radius
class Communicate(QObject):
    data_passed = pyqtSignal(Img2Conv)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = WebCamWidget(True)

    
    # 창의 크기와 제목 설정
    #ex.setGeometry(300, 300, 500, 400) # x, y 거리 x, y 크기 순 픽셀값
    ex.setWindowTitle("WebCamWidget smaple")
    ex.show()
    app.aboutToQuit.connect(ex.onExit)   
    sys.exit(app.exec_())