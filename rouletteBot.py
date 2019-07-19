from PIL import ImageGrab, ImageOps, Image
from numpy import *
from pytesseract import image_to_string
import pytesseract
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
isActive = False

# Player class
class Player:
    # player's money
    money = 0.0

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
    # winner secton
    winner = (845,864,845+50,864+50)

# Color Codes 
class ColorCodes:
    winner = 10395
    lose = 10246

# take a screenshot of position 'x_pad' and 'y_pad'
def screenGrab():
    box = (x_pad, y_pad, x_pad+990, y_pad+580)
    im = ImageGrab.grab(box)
    
    ##im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
    return im
# take a screenshot and turn it in grayscale and calculate a color code
def grab():
    box = (Cord.winner)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    #im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
    colorCode = array(im.getcolors())
    colorCode = colorCode.sum()
    print(colorCode)
    return colorCode

## CORDINATIONS
# get current mouse position x and y
def getCords():
    x,y = win32api.GetCursorPos()
    print(x,y)
# set cordinations
def saveCords(value):
    x,y = win32api.GetCursorPos()
    # filter value
    if value == 'chip_1':
        # save cord for chip 1€
        Cord.chip_1 = (x,y)
        time.sleep(.5)
        print('Position saved! X: '+ str(x) +' Y: '+ str(y))
    elif value == 'play':
        # save cord for play
        Cord.play = (x,y)
        time.sleep(.5)
        print('Position saved! X: '+ str(x) +' Y: '+ str(y))
    elif value == 'double':
        # save cord for double
        Cord.double = (x,y)
        time.sleep(.5)
        print('Position saved! X: '+ str(x) +' Y: '+ str(y))
    elif value == 'color_red':
        # save cord for color_red
        Cord.color_red = (x,y)
        time.sleep(.5)
        print('Position saved! X: '+ str(x) +' Y: '+ str(y))
    elif value == 'color_black':
        # save cord for color_black
        Cord.color_black = (x,y)
        time.sleep(.5)
        print('Position saved! X: '+ str(x) +' Y: '+ str(y))

## Money
# decrease money
def decreaseMoney():
    # decrease money
    Player.money -= 1.0
    print('Current Money: '+ str(Player.money))
# increase money
def increaseMoney():    
    # increase money
    Player.money += 1.0
    print('Current Money: '+ str(Player.money))

## Betting
# bet on red
def betRed(isLose=False):
    # You Lost - double it
    if isLose == True:
        # play double
        leftClick(Cord.double)
    # You Won
    else:
        # play red
        leftClick(Cord.color_red)
        time.sleep(.3)
        leftClick(Cord.play)
    time.sleep(.3)
    checkRound("red")
# bet on black
def betBlack(isLose=False):
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
    time.sleep(10)
    # red
    if color == "red":
        # check for color codes
        # if you lost
        print(grab())
        print(ColorCodes.winner)
        if grab() == ColorCodes.winner:
            # decrease money
            decreaseMoney()
            # play double
            print("Lose! Playing double...")
            betRed(True)
        # if you won
        elif grab() == ColorCodes.lose:
            # increase money
            increaseMoney()
            # play black
            print("Win! Playing black...")
            betBlack(False)
    # black
    elif color == "black":
        # check for color codes
        # if you lost
        print(grab())
        print(ColorCodes.winner)
        if grab() == ColorCodes.winner:
            # decrease money
            decreaseMoney()
            # play double
            print("Lose! Playing double...")
            betBlack(True)
        elif grab() == ColorCodes.lose:
            # increase money
            increaseMoney()
            # play red
            print("Win! Playing red...")
            betRed(False)

# set mouse to 'cord' position
def mousePos(cord):
    win32api.SetCursorPos((cord[0], cord[1]))

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
    time.sleep(.3)
    # click on location chip with number 1€
    leftClick(Cord.chip_1)
    time.sleep(.3)
    # begin with black
    betBlack(False)

## SETUP
def startConfig():
    print('This Bot is optimized for Bet365 page, if you want to use it somewhere else, try it out and let me know if it works.')
    print('-------------------------------------------')
    time.sleep(1.5)
    print('Starting configurating postions of the Roulette Game')
    print('-------------------------------------------')
    time.sleep(1)
    input('Move your Mouse Cursor on the \"1 Euro\" button and hit ENTER.')
    saveCords('chip_1')
    print('-------------------------------------------')
    time.sleep(.3)
    input('Move your Mouse Cursor on the \"Roll/Start\" button and hit ENTER.')
    saveCords('play')
    print('-------------------------------------------')
    time.sleep(.3)
    input('Move your Mouse Cursor on the \"Double and Play\" button and hit ENTER.')
    saveCords('double')
    print('-------------------------------------------')
    time.sleep(.3)
    input('Move your Mouse Cursor on the \"Red\" button and hit ENTER.')
    saveCords('color_red')
    print('-------------------------------------------')
    time.sleep(.3)
    input('Move your Mouse Cursor on the \"Black\" button and hit ENTER.')
    saveCords('color_black')
    print('-------------------------------------------')
    time.sleep(2)
    print('Thank you! Now we need your Money amount, so we can calculate if you won or lost!')
    time.sleep(.3)
    q_money = float(input('How much Money have you on your Hand? Enter like 20.0 : '))
    print('-------------------------------------------')
    print('Starting Bot in 3 seconds, don\'t change the size of the window, feel free to end the Bot with CTRL+C')
    time.sleep(3)
    #set money 
    Player.money = q_money
    time.sleep(1)
    gameStart()

if __name__ == '__main__':
    #gameStart()
    startConfig()
    #grab()
    #getCords()
    #getMoney()