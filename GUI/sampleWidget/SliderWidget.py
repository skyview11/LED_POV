import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSlider, QGridLayout

class SliderWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.init_value = 100
        self.range = (0, 500)
        self.labeltxt = "반지름"
        self.slider_dir = 1 # 1이면 수평 슬라이더, 2면 수직 슬라이더
        self.slider_value = 0
        self.init_ui()

    def init_ui(self):
        # 레이블, 슬라이더, 현재 볼륨을 표시하는 레이블 생성
        self.label = QLabel(f'{self.labeltxt}: ')
        self.slider = QSlider()
        self.value = QLabel(str(self.init_value)) 

        # 슬라이더의 범위 및 방향 설정
        self.slider.setRange(self.range[0], self.range[1])
        self.slider.setValue(self.init_value)
        self.slider.setOrientation(self.slider_dir)  

        # 레이아웃 생성 및 위젯 추가
        layout = QGridLayout()
        layout.addWidget(self.label, 0, 0)
        layout.addWidget(self.slider, 0, 1)
        layout.addWidget(self.value, 0, 2)

        # 위젯에 레이아웃 설정
        self.setLayout(layout)

        # 슬라이더의 값이 변경될 때 호출되는 함수 연결
        self.slider.valueChanged.connect(self.on_slider_changed)




    def on_slider_changed(self):
        # 슬라이더의 값이 변경될 때 호출되는 함수
        volume_value = self.slider.value()
        self.value.setText(str(volume_value))
        self.slider_value = volume_value

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SliderWidget()
    # 창의 크기와 제목 설정
    ex.setGeometry(300, 300, 300, 150)
    ex.setWindowTitle('Slider sample')
    ex.show()
    sys.exit(app.exec_())