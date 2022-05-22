import threading
from tkinter import Image
import cv2
import numpy as np
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Listener, KeyCode
import win32gui, win32ui, win32con
import schedule

TOGGLE_KEY = KeyCode(char = 'p')

clicking = False
mouse = MouseController()

def upgradeCapture():
    w = 1920
    h = 1080

    hwnd = None
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (w, h) , dcObj, (0, 0), win32con.SRCCOPY)

    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype = 'uint8')
    img.shape = (h, w, 4)

    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    return img

def ClickerUpgrade():
    mouse.position = (1629, 123)
    mouse.click(Button.left, 1)
    mouse.position = (289, 440)
    mouse.click(Button.left, 1)

def GoldenCookie():
    upgradeDisplayGC = upgradeCapture()
    img = upgradeDisplayGC, 0
    template = cv2.imread('goldencookietransp.png', 0)
    gh , gw = template.shape
    ##methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR, cv2.TM_CCOEFF_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]  
    img2 = cv2.cvtColor(upgradeDisplayGC, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(img2, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    location = max_loc

    bottom_right = (location[0] + gw, location[1] + gh)    
    cv2.rectangle(img2, location, bottom_right, 255, 5)
    cv2.namedWindow('Golden_Cookie_Match', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Golden_Cookie_Match', 960, 540)
    cv2.imshow('Golden_Cookie_Match', img2)
    GCx, GCy = max_loc
    mouse.position = (GCx + 50, GCy + 50)
    mouse.click(Button.left, 1)

schedule.every(1.5).minutes.do(ClickerUpgrade)
schedule.every(1.5).seconds.do(GoldenCookie)

def clicker():
    from time import time
    loop_time = time()
    while True:
        schedule.run_pending()
        if clicking: ##289 440
            mouse.position = (289, 440)
            mouse.click(Button.left, 1)

        upgradeDisplay = upgradeCapture()

        hsv = cv2.cvtColor(upgradeDisplay, cv2.COLOR_BGR2HSV)
        lower = np.array([60, 150, 20])
        upper = np.array([60, 160, 255])

        mask = cv2.inRange(hsv, lower, upper)

        contours, hierachy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) != 0:
            for contour in contours:
               if cv2.contourArea(contour) > 0:
                    x, y, w, h = cv2.boundingRect(contour) 
                    cv2.rectangle(upgradeDisplay, (x,y), (x + w, y + h), (0, 0, 255), 3)
                    M = cv2.moments(contour)

                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])

                    cv2.circle(upgradeDisplay, (cx, cy),7,(255, 0, 0), -1)
                    centerX = (cx)
                    centerY = (cy)
                    center = (cx, cy)
                    mouse.position = (centerX, centerY)
                    mouse.click(Button.left, 1)
                    print (center)
        
        cv2.namedWindow('Upgrade_Image', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('Upgrade_Image', 960, 540)
        cv2.imshow('Upgrade_Image', upgradeDisplay)

        cv2.waitKey(1)
        print('FPS {}'.format(1 / (time() - loop_time))) 
        loop_time = time()

def toggle_event(key):
    if key == TOGGLE_KEY:
        global clicking
        clicking = not clicking

click_thread = threading.Thread(target = clicker)
click_thread.start()

with Listener(on_press = toggle_event) as listener:
    listener.join()

print('Done.')