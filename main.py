#!/usr/bin/env python
import cv2
import numpy as np
import pyautogui
import os 

from PIL import ImageGrab, ImageDraw
import pygetwindow as gw
import time

#screenshot = ImageGrab.grab()
#draw = ImageDraw.Draw(screenshot)

def main():
    import MemoryWork
    #screen = takeScreenShot()
    #LookForPathToWalk()

    return 0

def CreateBoxVisual(x,y,height,width):
    box_color = (255,0,0) #Rot
    #draw.rectangle([x,y,x+height,y+width],outline=box_color)
    
    return 0

def takeScreenShot():
    screen = pyautogui.screenshot()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    screen.save(dir_path+'\screenshot_1.png')
    return screen

def LookForPathToWalk():
    for found in pyautogui.locateAllOnScreen('Test1.png',confidence=0.9):
        if(found == None):
            return
        print(found)
        CreateBoxVisual(found[0],found[1],found[2],found[3])
    
    #screenshot.show()

    Paths = [[0,0],[0,0]]
    return 0


if __name__ == "__main__":
    main()
