import cv2
import sys, os
from time import time
#from opt import args
from math import pi, cos, sin
import numpy as np
from scipy.interpolate import LinearNDInterpolator
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from GUI.sampleWidget.WebCamWidget import Img2Conv

# 이미지를 입력받아서 신호 당 위치당 출력을 txt로 반환하는 함수 제작
class Img2POV:
    def __init__(self, n_led=32, encoder_resolution=380):
        self.n_led = n_led
        self.encoder_resolution = encoder_resolution
        self.outlist = []
        self.auto = True
    def readImg_str(self, img_path: str):
        self.img = cv2.imread(img_path)
        self.center = (self.img.shape[0]//2, self.img.shape[1]//2)
        self.radius = min(self.center)
        self.idxs = self.__getIdxs__()
        
    def readImg_pov(self, img: Img2Conv):
        self.img = img.image
        self.center = img.center
        self.radius = img.radius
        self.idxs = self.__getIdxs__()
    def writeTxt(self, filename):
        with open(filename, 'w') as f:
            f.write("# number of LED, resolution of motor encoder \n")
            f.write(f"{self.n_led}, {self.encoder_resolution} \n")
            for line in self.outlist:
                f.write(self.__list2str(line))
                
    # util functions         
    def __makeInterpFunc__(self):
        n_row, n_col, n_ch = self.img.shape
        print(n_row, n_col, self.img.shape)
        coords = []
        t = time()
        for r in range(n_row):
            for c in range(n_col):
                coords.append([r, c])
        print(f"for문: {time() - t}")
        t = time()
        points = np.array(coords)
        values = self.img.reshape(-1, n_ch)
        print(points.shape, values.shape)
        print(f" point, value 가공: {time() - t}")
        t = time()
        interp = LinearNDInterpolator(points, values)
        print(f"interp 생성: {time() - t}")
        return interp
                
        
    def __getIdxs__(self):
        theta = np.linspace(0, 2*np.pi, self.encoder_resolution+1)[:-1].reshape(self.encoder_resolution, 1)
        l = np.linspace(0, self.radius, self.n_led+1)[1:].reshape(1, self.n_led)
        rows = np.clip(self.center[0] - (np.cos(theta) @ l), 0, self.img.shape[0]-2)
        cols = np.clip(self.center[1] + (np.sin(theta) @ l), 0, self.img.shape[1]-2)
        
        return np.concatenate((rows[:, :, None], cols[:, :, None]), axis=2)
        
    
    def get_colors(self):
        points = self.idxs.reshape(-1, 2)
        for i in range(points.shape[0]):
            row = int(points[i, 0])
            col = int(points[i, 1])
            self.outlist.append(self.img[row, col])    
                   
    def __list2str(self, arr):
        out = ""
        for word in arr:
            out = out + str(word) + " "
        out += "\n"
        return out
    
        

                
            

if __name__ == "__main__":
    t_i = time()
    imgpath = "../winxp.jpg"
    img = Img2POV(32, 380)
    t_1 = time()
    img.readImg_str(imgpath)
    t_2 = time()
    img.get_colors()
    t_3 = time()
    img.writeTxt("test.txt")
    t_f = time()
    print(f"시간: {t_f-t_i} \n fps: {1/(t_f-t_i)}")
    print(f"time : object init: {t_1 - t_i}, readimg: {t_2 - t_1}, get_colors: {t_3 - t_2}, writeTxt: {t_f - t_3}")
    print(f"fps  : object init: inf, readimg: {1/(t_2 - t_1)}, get_colors: {1/(t_3 - t_2)}, writeTxt: {1/(t_f - t_3)}")
    