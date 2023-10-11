import sys
from .sampleWidget import *
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout




class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        
        
        
        self.init_ui()
        
    def init_ui(self):
        # 카메라, 슬라이드 바 불러오기
        self.video = WebCamWidget()
        self.slider = SliderWidget()
        self.btn_camOn = QPushButton("cam on")
        self.btn_camOff = QPushButton("cam off")
        self.btn_povOn = QPushButton("pov on")
        self.btn_povOff = QPushButton("pov off")
        self.title = QLabel("LED POV")
        # 버튼이 변경될 때 호출되는 함수 설정
        self.btn_camOn.clicked.connect(self.__camOn)
        self.btn_camOff.clicked.connect(self.__camOff)
        self.btn_povOn.clicked.connect(self.__povOn)
        self.btn_povOff.clicked.connect(self.__povOff)
        self.slider.slider.valueChanged.connect(self.__getR)
        
        
        # 레이아웃 생성 및 위젯 추가
        layout = QGridLayout()
        layout.addWidget(self.title, 0, 0)
        layout.addWidget(self.video, 1, 0)
        layout.addWidget(self.slider, 2, 0)
        layout.addWidget(self.btn_camOn, 3, 0)
        layout.addWidget(self.btn_camOff, 3, 1)
        layout.addWidget(self.btn_povOn, 4, 0)
        layout.addWidget(self.btn_povOff, 4, 1)
        
        self.setLayout(layout)
    def __getR(self):
        self.video.r = self.slider.slider.value()
    def __camOn(self):
        self.video.readCamAtive(True)
    def __camOff(self):
        self.video.readCamAtive(False)
    def __povOn(self):
        pass
    def __povOff(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWidget()

    
    # 창의 크기와 제목 설정
    #ex.setGeometry(300, 300, 500, 400) # x, y 거리 x, y 크기 순 픽셀값
    ex.setWindowTitle("mainWIndow smaple")
    ex.show()
    app.aboutToQuit.connect(ex.video.onExit)   
    sys.exit(app.exec_())