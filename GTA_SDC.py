import numpy as np
from PIL import ImageGrab
import cv2
import time
from directkeys import PressKey, ReleaseKey, W,A,S,D


def main():
    for i in range(0,5):
        print(i)
        time.sleep(1)

    PressKey(W)
    ReleaseKey(W)

def draw_lines(p_img, lines):
    try:
        for line in lines:
            coords = line[0]
            cv2.line(p_img,(coords[0],coords[1]),(coords[2],coords[3]),[255,255,255],3)

    except:
        pass

def region_of_interest(img,vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask,vertices,255)
    masked = cv2.bitwise_and(img,mask)
    return masked

def process_img(og_img):
    p_img = cv2.cvtColor(og_img,cv2.COLOR_BGR2GRAY)
    p_img = cv2.Canny(p_img,threshold1=200,threshold2=300)
    p_img  = cv2.GaussianBlur(p_img,(5,5),0)
    contours, hierarchy = cv2.findContours(p_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    p_img = cv2.drawContours(p_img, contours, -1, (0, 255, 75), 2)
    verticies = np.array([[10,500],[10,300],[300,200],[500,200],[800,300],[800,500],[500,350],[300,350]],np.int32)
    p_img = region_of_interest(p_img,[verticies])

    lines = cv2.HoughLinesP(p_img,1,np.pi/180,180,np.array([]),100,5)
    draw_lines(p_img,lines)

    return p_img

lastT = time.time()
while(True):
        screen= np.array(ImageGrab.grab(bbox=(0,40,800,640)))
        new_screen = process_img(screen)

        print('{}'.format(time.time()-lastT))
        lastT = time.time()
        cv2.imshow('window',new_screen)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyWindow()
            break