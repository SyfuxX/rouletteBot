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
from pynput import *

# Globals
# ----------------
keyboard = keyboard
mouse = mouse
x_pad = 455
y_pad = 345
isActive = False
loseMultiplicator = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
winMultiplicator = [0, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]

# Settings class
class Settings:
    # money
    money = False
    # chip 1
    chip_1 = False
    # start button
    start = False
    # double button
    double = False
    # red field
    red = False
    # black field
    black = False
    # loser section
    loserSection = False
    # start by black/red
    redOrBlack = 0

# Player class
class Player:
    # player's money
    money = 0.0
    # player's lose counter
    loseCounter = 0
    currentLose = 1.0

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
    # loser secton
    loser = (845,864,845+50,864+50)

# Color Codes 
class ColorCodes:
    lose = 10246

## CLEAR CONSOLE
clear = lambda: os.system('cls')

# take a screenshot of position 'x_pad' and 'y_pad'
def screenGrab():
    box = (x_pad, y_pad, x_pad+990, y_pad+580)
    im = ImageGrab.grab(box)
    
    ##im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
    return im
# take a screenshot and turn it in grayscale and calculate a color code
def grab():
    box = (Cord.loser)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    #im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
    colorCode = array(im.getcolors())
    colorCode = colorCode.sum()
    #print(colorCode)
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
    elif value == 'loser':
        # save cord for loser section
        Cord.loser = (x,y,x+50,y+50)
        time.sleep(.1)
        print('Position saved! X: '+ str(x) +' Y: '+ str(y) +' Zone: +50')

## Money
# decrease money
def decreaseMoney():
    # decrease money
    Player.money = Player.money - loseMultiplicator[Player.loseCounter]
    # print out current Money after lose
    print('You lost! Your money: '+ str(Player.money) +'€')
    # increase loseCounter
    Player.loseCounter += 1
# increase money
def increaseMoney():
    # increase money by winMultiplicator
    Player.money = Player.money + winMultiplicator[Player.loseCounter]
    # print out current Money after win
    print('You won! Your money: '+ str(Player.money) +'€')

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
        print(grab())
        print(ColorCodes.lose)
        # check for color codes
        # if you lost
        if grab() == ColorCodes.lose:
            # decrease money
            decreaseMoney()
            # play double
            print("Playing again with double ...")
            betRed(True)
        # if you won
        elif grab() != ColorCodes.lose:
            # increase money
            increaseMoney()
            # play black
            print("Playing now on black ...")
            betBlack(False)
    # black
    elif color == "black":
        print(grab())
        print(ColorCodes.lose)
        # check for color codes
        # if you lost
        if grab() == ColorCodes.lose:
            # decrease money
            decreaseMoney()
            # play double
            print("Playing again with double ...")
            betBlack(True)
        # if you won
        elif grab() != ColorCodes.lose:
            # increase money
            increaseMoney()
            # play red
            print("Playing now on red ...")
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
    # check if all settings are set
    if (Settings.money == True and Settings.chip_1 == True and Settings.double == True and Settings.loserSection == True and Settings.redOrBlack != 0 and Settings.start == True and Settings.color_black == True and Settings.color_red == True):
        # start game
        time.sleep(.3)
        # click on location chip with number 1€
        leftClick(Cord.chip_1)
        time.sleep(.3)
        if (Settings.redOrBlack == 1):
            # begin with black
            betBlack(False)
        else:
            # begin with red
            betRed(False)
    else:
        clear()
        print("You have not configurated the Bot yet!")
        time.sleep(2)
        menu()

## KEYBOARD LISTENERS
# on press
def configMenu(key):
    if key == 1:
        clear()
        # change money amount
        print('Enter like:')
        print('5€ = 5.0')
        print('10€ = 10.0')
        print('25,50€ = 25.5')
        Settings.money = True
        time.sleep(.1)
        Player.money = float(input('Money in your Hand? '))
        settingsInfo()
    elif key == 2:
        clear()
        # save position for roll/start
        print('Wait for saving position for Play button ...')
        Settings.start = True
        time.sleep(.1)
        saveCords('play')
        settingsInfo()
    elif key == 3:
        clear()
        # save position for double
        print('Wait for saving position for Double button ...')
        Settings.double = True
        time.sleep(.1)
        saveCords('double')
        settingsInfo()
    elif key == 4:
        clear()
        # save position for color red
        print('Wait for saving position for Red color ...')
        Settings.red = True
        time.sleep(.1)
        saveCords('color_red')
        settingsInfo()
    elif key == 5:
        clear()
        # save position for color black
        print('Wait for saving position for Black color ...')
        Settings.black = True
        time.sleep(.1)
        saveCords('color_black')
        settingsInfo()
    elif key == 6:
        clear()
        # save position for chip 1€
        print('Wait for saving position for 1 Euro Chip ...')
        Settings.chip_1 = True
        time.sleep(.1)
        saveCords('chip_1')
        settingsInfo()
    elif key == 7:
        clear()
        # change loser section
        print('Wait for saving position for Loser Section ...')
        Settings.loserSection = True
        time.sleep(.1)
        saveCords('loser')
        saveColor = grab()
        ColorCodes.lose = saveColor
        settingsInfo()
    elif key == 8:
        clear()
        # change start by black or red
        print('Choose the starting Bet:')
        print('Black = 1')
        print('Red = 2')
        time.sleep(.1)
        Settings.redOrBlack = int(input('Start with Black or Red? '))
        settingsInfo()
    elif key == 0:
        print('All Settings has been saved, back to main menu ...')
        time.sleep(1)
        menu()

## MENUS
# Menu
def menu():
    clear()
    print('######################')
    print('## ROULETTE BOT MENU')
    print('######################')
    time.sleep(.1)
    print('## NAVIGATION OPTION')
    print('######################')
    time.sleep(.1)
    print('## [1] - Start Bot')
    print('## [2] - Configurate Bot')
    print('##')
    print('## [9] - Open About')
    print('## [0] - Exit')
    print('#######################')
    time.sleep(.3)
    # navigate to settings
    menu_nav = input('Select an option [1|2|9|0] and hit ENTER: ')
    # if 1
    if menu_nav == '1':
        # start bot
        gameStart()
    if menu_nav == '2':
        # start config
        startConfig()
    if menu_nav == '9':
        # start about
        startAbout()
    if menu_nav == '0':
        # exit
        exit()
# Config
def startConfig():
    clear()
    settingsInfo()
# About
def startAbout():
    clear()
    # about me
    print('######################')
    print('## ABOUT ROULETTEBOT')
    print('######################')
    print('## Bot was created by SyfuxX!')
    print('## Thank you for using it.')
    time.sleep(.1)
    print('######################')
    print('## NAVIGATION OPTION')
    print('######################')
    time.sleep(.1)
    print('## [1] - Back to Main Menu')
    print('##')
    print('## [0] - Exit')
    print('#######################')
    time.sleep(.3)
    # navigate to settings
    menu_nav = input('Select an option [1|0] and hit ENTER: ')
    if menu_nav == '1':
        # start about
        menu()
    if menu_nav == '0':
        # exit
        exit()
# Settings Info
def settingsInfo():
    time.sleep(1)
    clear()
    print('#######################')
    # check if 'money' is set
    if Settings.money == True:
        print('## [1] - Money Amount [X] - '+ str(Player.money) +'€')
    else:
        print('## [1] - Money Amount [ ]')
    # check if 'play' is set
    if Settings.start == True:
        print('## [2] - Start Button [X] - '+ str(Cord.play))
    else:
        print('## [2] - Start Button [ ]')
    # check if 'double' is set
    if Settings.double == True:
        print('## [3] - Double Button [X] - '+ str(Cord.double))
    else:
        print('## [3] - Double Button [ ]')
    # check if 'red' is set
    if Settings.red == True:
        print('## [4] - Red Field [X] - '+ str(Cord.color_red))
    else:
        print('## [4] - Red Field [ ]')
    # check if 'black' is set
    if Settings.black == True:
        print('## [5] - Black Field [X] - '+ str(Cord.color_black))
    else:
        print('## [5] - Black Field [ ]')
    # check if 'chip 1' is set
    if Settings.chip_1 == True:
        print('## [6] - Chip 1 Euro [X] - '+ str(Cord.chip_1))
    else:
        print('## [6] - Chip 1 Euro [ ]')
    # check if 'loser section' is set
    if Settings.loserSection == True:
        print('## [7] - Loser Section [X] - '+ str(Cord.loser))
    else:
        print('## [7] - Loser Section [ ]')
    # change start by black or red
    if Settings.redOrBlack == 2:
        print('## [8] - Start with Black/Red [X] - Red')
    elif Settings.redOrBlack == 1:
        print('## [8] - Start with Black/Red [X] - Black')
    else:
        print('## [8] - Start with Black/Red [ ]')
    print('##')
    print('## [0] - Save Config')
    print('#######################')
    time.sleep(.1)
    option = int(input("Select an option [1|2|3|4|5|6|7|8|0] and hit ENTER: "))
    configMenu(option)
    
if __name__ == '__main__':
    menu()
    #grab()