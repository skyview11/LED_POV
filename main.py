import sys
from GUI.mainWindow import MainWidget
from PyQt5.QtWidgets import QApplication
from time import time
from Logic import *

init_t = time()

def get_data(data):
    converter = Img2POV()
    print(data.image.shape, data.center, data.radius)
    converter.readImg_pov(data)
    converter.get_colors()
    #converter.writeTxt("./trash/" + str(round(time()-init_t, 3)) + ".txt")
    return data
if __name__ == "__main__":
    t_i = time()
    app = QApplication(sys.argv)
    ex = MainWidget()
    ex.setWindowTitle("mainWIndow smaple")
    ex.show()
    app.aboutToQuit.connect(ex.video.onExit)   
    data = ex.video.communicator.data_passed.connect(get_data)
    print(data)
    sys.exit(app.exec_())