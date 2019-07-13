from PIL import ImageGrab, ImageOps, Image
from numpy import *
from pytesseract import image_to_string
import pytesseract
import array
import os
import time
import win32api
import win32con
import pyautogui
import numbers

# Globals
# ----------------
x_pad = 455
y_pad = 345
money = "0.0"
oldMoney = "0.0"
isActive = False

# Cord class with cordinations in
class Cord:
    # chip section
    chip_1 = (96,283)
    # bet section
    color_red = (445,483)
    color_black = (546,484)
    # play menu section
    play = (893,462)
    double = (893,373)

# take a screenshot of position 'x_pad' and 'y_pad'
def screenGrab():
    box = (x_pad, y_pad, x_pad+990, y_pad+580)
    im = ImageGrab.grab(box)
    
    ##im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
    return im

# get current mouse position x and y
def getCords():
    x,y = win32api.GetCursorPos()
    x = x - x_pad
    y = y - y_pad
    print(x,y)

## Money
# read out money
def getMoney(pos="pos1"):
    global money
    currentPos = pos
    # if try pos1
    if pos == "pos1":
        pos1 = pyautogui.screenshot('money.png',region=(x_pad+42,y_pad+560,100,30))
        time.sleep(1)
        img = Image.open('money.png')
        pos1 = pytesseract.image_to_string(img)
        money = pos1
    # try different position
    elif pos == "pos2":
        pos2 = pyautogui.screenshot('money.png',region=(x_pad+35,y_pad+560,100,30))
        time.sleep(1)
        img = Image.open('money.png')
        pos2 = pytesseract.image_to_string(img)
        money = pos2[1:]
    # try different position
    elif pos == "pos3":
        pos3 = pyautogui.screenshot('money.png',region=(x_pad+128,y_pad+535,100,20))
        time.sleep(1)
        img = Image.open('money.png')
        pos3 = pytesseract.image_to_string(img)
        money = pos3
    time.sleep(.5)
    print(money)
    # check if money is not empty
    try:
        if float(money):
            print("Your current Money is: "+ money +"€")
            return money
    except ValueError:    
        print("Can't read your Money! Trying again...")
        time.sleep(.5)
        if currentPos == "pos1":
            # do again
            getMoney("pos2")
        elif currentPos == "pos2":
            # do again
            getMoney("pos3")
# save money
def saveMoney(value):
    global oldMoney
    oldMoney = value
    return oldMoney

## Betting
# bet on red
def betRed(isLose=False):
    # save money
    saveMoney(money)
    # check if 'isLose' true - so double it
    if isLose == True:
        # play double
        leftClick(Cord.double)
    elif isLose == False:
        # play red
        leftClick(Cord.color_red)
        time.sleep(.3)
        leftClick(Cord.play)
    time.sleep(.3)
    checkRound("red")
# bet on black
def betBlack(isLose=False):
    # save money
    saveMoney(money)
    # check if 'isLose' true - so double it
    if isLose == True:
        # play double
        leftClick(Cord.double)
    elif isLose == False:
        # play black
        leftClick(Cord.color_black)
        time.sleep(.3)
        leftClick(Cord.play)
    time.sleep(.3)
    checkRound("black")

# check round if you lost it or won it
def checkRound(color):
    global money, oldMoney
    time.sleep(7.5)
    getMoney()
    time.sleep(.3)
    # red
    if color == "red":
        # if you lost
        if money < oldMoney:
            # play double
            print("Lose! Playing double...")
            betRed(True)
        elif money > oldMoney:
            # play black
            print("Win! Playing black...")
            betBlack(False)
    # black
    elif color == "black":
        # if you lost
        if money < oldMoney:
            # play double
            print("Lose! Playing double...")
            betBlack(True)
        elif money > oldMoney:
            # play red
            print("Win! Playing red...")
            betRed(False)
    time.sleep(.3)
    saveMoney(getMoney())

# set mouse to 'cord' position
def mousePos(cord):
    win32api.SetCursorPos((x_pad + cord[0], y_pad + cord[1]))

# do a left mouse click
def leftClick(cord):
    #set location
    mousePos((cord))
    time.sleep(.3)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.3)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(.3)
    print("Click!")

# start the Game
def gameStart():
    global isActive, money
    isActive = True
    # get money
    getMoney()
    time.sleep(.3)
    # click on location chip with number 1€
    leftClick(Cord.chip_1)
    time.sleep(.3)
    # begin with black
    betBlack(False)

if __name__ == '__main__':
    gameStart()
    #getCords()
    #getMoney()