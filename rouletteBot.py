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

# Settings class
class Settings:
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
    # money
    money = False
    # loser section
    loserSection = False

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
    im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
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
    elif value == 'loser':
        # save cord for loser section
        Cord.loser = (x,y,x+50,y+50)
        time.sleep(.1)
        print('Position saved! X: '+ str(x) +' Y: '+ str(y) +' Zone: +50')

## Money
# decrease money
def decreaseMoney():
    # increase loseCounter
    Player.loseCounter += 1
    # decrease by loseCounter
    if Player.loseCounter == 1:
        # decrease money
        Player.money -= 1.0
    elif Player.loseCounter > 1:
        # save currentLose
        Player.currentLose = Player.currentLose*2
    print('loseCounter: '+ str(Player.loseCounter))
    print('currentLose: '+ str(Player.currentLose))
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
        print(grab())
        print(ColorCodes.lose)
        # check for color codes
        # if you lost
        if grab() == ColorCodes.lose:
            # decrease money
            decreaseMoney()
            # play double
            print("Lose! Playing again with double ...")
            betRed(True)
        # if you won
        elif grab() != ColorCodes.lose:
            # increase money
            increaseMoney()
            # play black
            print("Win! Playing now on black ...")
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
            print("Lose! Playing again with double ...")
            betBlack(True)
        # if you won
        elif grab() != ColorCodes.lose:
            # increase money
            increaseMoney()
            # play red
            print("Win! Playing now on red ...")
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

## KEYBOARD LISTENERS
# on press
def on_press(key):
    if key == keyboard.KeyCode.from_char('1'):
        clear()
        # save position for chip 1€
        print('Wait for saving position for 1 Euro Chip ...')
        Settings.chip_1 = True
        time.sleep(.1)
        saveCords('chip_1')
        settingsInfo()
    elif key == keyboard.KeyCode.from_char('2'):
        clear()
        # save position for roll/start
        print('Wait for saving position for Play button ...')
        Settings.start = True
        time.sleep(.1)
        saveCords('play')
        settingsInfo()
    elif key == keyboard.KeyCode.from_char('3'):
        clear()
        # save position for double
        print('Wait for saving position for Double button ...')
        Settings.double = True
        time.sleep(.1)
        saveCords('double')
        settingsInfo()
    elif key == keyboard.KeyCode.from_char('4'):
        clear()
        # save position for color red
        print('Wait for saving position for Red color ...')
        Settings.red = True
        time.sleep(.1)
        saveCords('color_red')
        settingsInfo()
    elif key == keyboard.KeyCode.from_char('5'):
        clear()
        # save position for color black
        print('Wait for saving position for Black color ...')
        Settings.black = True
        time.sleep(.1)
        saveCords('color_black')
        settingsInfo()
    elif key == keyboard.KeyCode.from_char('6'):
        clear()
        # change money amount
        print('Wait for saving Money from your Hand ...')
        Settings.money = True
        time.sleep(.1)
        Player.money = float(input('Money in your Hand? Enter like 20.0: '))
        settingsInfo()
    elif key == keyboard.KeyCode.from_char('7'):
        clear()
        # change loser section
        print('Wait for saving position for Loser Section ...')
        Settings.loserSection = True
        time.sleep(.1)
        saveCords('loser')
        saveColor = grab()
        ColorCodes.lose = saveColor
        settingsInfo()
    elif key == keyboard.Key.esc:
        print('All Settings has been saved, back to main menu ...')
        time.sleep(1)
        menu()
        return False

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
    print('## Start Bot [1]')
    print('## Configurate Bot [2]')
    print('##')
    print('## Open About [9]')
    print('## Exit [0]')
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
    # listen to key press events
    with keyboard.Listener(on_press=on_press) as listener:
        try:
            listener.join()
        except MyError as e:
            print('{0} was pressed'.format(e.args[0]))
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
    print('## Back to Main Menu [1]')
    print('##')
    print('## Exit [0]')
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
    print('#######################')
    # check if 'chip 1' is set
    if Settings.chip_1 == True:
        print('## Chip 1 Euro [X]')
    else:
        print('## Chip 1 Euro [ ] - Hit Key \'1\' to configurate')
    # check if 'play' is set
    time.sleep(.1)
    if Settings.start == True:
        print('## Start Button [X]')
    else:
        print('## Start Button [ ] - Hit Key \'2\' to configurate')
    # check if 'double' is set
    time.sleep(.1)
    if Settings.double == True:
        print('## Double Button [X]')
    else:
        print('## Double Button [ ] - Hit Key \'3\' to configurate')
    # check if 'red' is set
    time.sleep(.1)
    if Settings.red == True:
        print('## Red Field [X]')
    else:
        print('## Red Field [ ] - Hit Key \'4\' to configurate')
    # check if 'black' is set
    time.sleep(.1)
    if Settings.black == True:
        print('## Black Field [X]')
    else:
        print('## Black Field [ ] - Hit Key \'5\' to configurate')
    # check if 'money' is set
    time.sleep(.1)
    if Settings.money == True:
        print('## Money Amount [X]')
    else:
        print('## Money Amount [ ] - Hit Key \'6\' to configurate')
    # check if 'loser section' is set
    time.sleep(.1)
    if Settings.loserSection == True:
        print('## Loser Section [X]')
    else:
        print('## Loser Section [ ] - Hit Key \'7\' to configurate')
    print('## Hit Key \'ESC\' to save config')
    print('#######################')
    time.sleep(1)

if __name__ == '__main__':
    menu()
    #grab()