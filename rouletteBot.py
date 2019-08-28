from PIL import ImageGrab, ImageOps, Image
from numpy import *
from pytesseract import image_to_string
import pytesseract
import os
import io
import configparser
import time
import win32api
import win32con
import pyautogui
import numbers
from pynput import *

# Game Logics
# ----------------
# Bet365
# 1. Click on "1€" Chip
# 2. Click on "Red or Black"
# 3. Click on "Start"
# 4. Wait 10 seconds and take a screenshot of "Loser Section"
# - Losing
# 1. Click on "Double and Start"
# - Winning
# 1. Click on "Red or Black", depends which you played before
# 2. Click on "Start"
# --
# CasinoClub
# 1. Click on "Take Place"
# 2. Click on "1€" Chip
# 3. Click on "Red or Black"
# 4. Click on "Start"
# 5. Wait 15 seconds and take a screenshot of "Loser Section"
# - Losing
# 1. Click on "Start" and place same amount of chips as the round before [Only Coordination of Start]
# 2. Click on "Red or Black", depends which you played before and hit it x times [x = loseCounter]
# 3. Click on "Start"
# - Winning
# 1. Click on "Red or Black", depends which you played before
# 2. Click on "Start"

# Globals
# ----------------
keyboard = keyboard
mouse = mouse
Config = configparser.ConfigParser(strict=False)
x_pad = 455
y_pad = 345
isActive = False
loseMultiplicator = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
winMultiplicator = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
hashLine = "######################"
configName = "config.ini"

# Settings class
class Settings:
    # money [All]
    money = False
    # chip 1 [All]
    chip_1 = False
    # start button [All]
    start = False
    # double button [Bet365]
    double = False
    # red field [All]
    red = False
    # black field [All]
    black = False
    # loser section [All]
    loserSection = False
    # start by black/red [All]
    redOrBlack = 0
    # webpage / software
    casino = ""

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
    chip_1_f = 0
    chip_1_s = 0
    chip_1 = (0,0)
    # bet section
    color_red_f = 0
    color_red_s = 0
    color_red = (0,0)
    color_black_f = 0
    color_black_s = 0
    color_black = (0,0)
    # play menu section
    play_f = 0
    play_s = 0
    play = (0,0)
    double_f = 0
    double_s = 0
    double = (0,0)
    # loser secton
    loser_f = 0
    loser_s = 0
    loser_t = 0
    loser_fo = 0
    loser = (0,0,0,0)

# Color Codes 
class ColorCodes:
    lose = 10246

## CLEAR CONSOLE
clear = lambda: os.system('cls')

# Take a screenshot of position 'x_pad' and 'y_pad'
def screenGrab():
    box = (x_pad, y_pad, x_pad+990, y_pad+580)
    im = ImageGrab.grab(box)
    
    #im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
    return im
# Take a screenshot and turn it in grayscale and calculate a color code
def grab():
    box = (Cord.loser)
    im = ImageOps.grayscale(ImageGrab.grab(box))
    #im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) + '.png', 'PNG')
    colorCode = array(im.getcolors())
    colorCode = colorCode.sum()
    #print("Color Code: "+ str(colorCode))
    return colorCode

## CORDINATIONS
# Get current mouse position x and y
def getCords():
    x,y = win32api.GetCursorPos()
    print(x,y)
# Set cordinations
def saveCords(value):
    x,y = win32api.GetCursorPos()
    # filter value
    if value == 'chip_1':
        # save cord for chip 1€
        Cord.chip_1_f = x
        Cord.chip_1_s = y
        Cord.chip_1 = (Cord.chip_1_f,Cord.chip_1_s)
        time.sleep(.5)
        print('## [INFO] - Position saved! X: '+ str(x) +' Y: '+ str(y))
    elif value == 'play':
        # save cord for play
        Cord.play_f = x
        Cord.play_s = y
        Cord.play = (Cord.play_f,Cord.play_s)
        time.sleep(.5)
        print('## [INFO] - Position saved! X: '+ str(x) +' Y: '+ str(y))
    elif value == 'double':
        # save cord for double
        Cord.double_f = x
        Cord.double_s = y
        Cord.double = (Cord.double_f,Cord.double_s)
        time.sleep(.5)
        print('## [INFO] - Position saved! X: '+ str(x) +' Y: '+ str(y))
    elif value == 'color_red':
        # save cord for color_red
        Cord.color_red_f = x
        Cord.color_red_s = y
        Cord.color_red = (Cord.color_red_f,Cord.color_red_s)
        time.sleep(.5)
        print('## [INFO] - Position saved! X: '+ str(x) +' Y: '+ str(y))
    elif value == 'color_black':
        # save cord for color_black
        Cord.color_black_f = x
        Cord.color_black_s = y
        Cord.color_black = (Cord.color_black_f,Cord.color_black_s)
        time.sleep(.5)
        print('## [INFO] - Position saved! X: '+ str(x) +' Y: '+ str(y))
    elif value == 'loser':
        # Bet365
        if (Settings.casino == "Bet365"):
            Cord.loser_f = x
            Cord.loser_s = y
            Cord.loser_t = x+50
            Cord.loser_fo = y+50
            Cord.loser = (Cord.loser_f,Cord.loser_s,Cord.loser_t,Cord.loser_fo)
        # CasinoClub
        elif (Settings.casino == "CasinoClub"):
            Cord.loser_f = x
            Cord.loser_s = y
            Cord.loser_t = x+50
            Cord.loser_fo = y+12
            Cord.loser = (Cord.loser_f,Cord.loser_s,Cord.loser_t,Cord.loser_fo)
        # save cord for loser section
        time.sleep(.1)
        print('Position saved! X: '+ str(x) +' Y: '+ str(y) +' Zone: +50')

## Money
# Decrease money
def decreaseMoney():
    print(hashLine)
    # decrease money
    Player.money = Player.money - loseMultiplicator[Player.loseCounter]
    # print out current Money after lose
    print('## [INFO] - LOSE! Money: '+ str(Player.money) +'€')
    # increase loseCounter
    Player.loseCounter += 1
# Increase money
def increaseMoney():
    print(hashLine)
    # increase money by winMultiplicator
    Player.money = Player.money + winMultiplicator[Player.loseCounter]
    # print out current Money after win
    print('## [INFO] - WIN! Money: '+ str(Player.money) +'€')
    # reset loseCounter
    Player.loseCounter = 0

## BETTING
# Bet on red
def betRed(isLose=False):
    # check if 'Player.loseCounter' is bigger than 0
    if (Player.loseCounter > 0):
        # decrease by 1
        clickMulti = Player.loseCounter-1
    elif (Player.loseCounter == 0):
        # increase by 1
        clickMulti = Player.loseCounter+1
    clickCounter = loseMultiplicator[clickMulti]
    print("## [DEBUG] - Click Counter: "+ str(clickCounter))
    i = 0
    # Bet365
    if (Settings.casino == "Bet365"):
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
    # CasinoClub
    elif (Settings.casino == "CasinoClub"):
        # You Lost - double it
        if isLose == True:
            # click on 'Same Amount' [Play]
            leftClick(Cord.play)
            # click on 'Red' x times [x = loseCounter]
            for i in range(clickCounter):
                time.sleep(.3)
                leftClick(Cord.color_red)
            time.sleep(.3)
            # click on 'Play'
            leftClick(Cord.play)
        # You Won
        else:
            # bet on red
            leftClick(Cord.color_red)
            time.sleep(.3)
            # play
            leftClick(Cord.play)
        time.sleep(.3)
        checkRound("red")

# Bet on black
def betBlack(isLose=False):
    # check if 'Player.loseCounter' is bigger than 0
    if (Player.loseCounter > 0):
        # decrease by 1
        clickMulti = Player.loseCounter-1
    elif (Player.loseCounter == 0):
        # increase by 1
        clickMulti = Player.loseCounter+1
    clickCounter = loseMultiplicator[clickMulti]
    print("## [DEBUG] - Click Counter: "+ str(clickCounter))
    i = 0
    # Bet365
    if (Settings.casino == "Bet365"):
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
    # CasinoClub
    elif (Settings.casino == "CasinoClub"):
        # You Lost - double it
        if isLose == True:
            # click on 'Same Amount' [Play]
            leftClick(Cord.play)
            # click on 'Black' x times [x = loseCounter]
            for i in range(clickCounter):
                time.sleep(.3)
                leftClick(Cord.color_black)
            time.sleep(.3)
            # click on 'Play'
            leftClick(Cord.play)
        # You Won
        else:
            # bet on black
            leftClick(Cord.color_black)
            time.sleep(.3)
            # play
            leftClick(Cord.play)
        time.sleep(.3)
        checkRound("black")

# Check round if you lost it or won it
def checkRound(color):
    i = 0
    # Bet365
    if (Settings.casino == "Bet365"):
        i = 12
    # CasinoClub
    elif (Settings.casino == "CasinoClub"):
        i = 30
    time.sleep(i)
    # red
    if color == "red":
        # check for color codes
        # if you lost
        if grab() == ColorCodes.lose:
            # decrease money
            decreaseMoney()
            # play double
            print("## [INFO] - Playing again with double ...")
            betRed(True)
        # if you won
        elif grab() != ColorCodes.lose:
            # increase money
            increaseMoney()
            # play black
            print("## [INFO] - Playing now on black ...")
            betBlack(False)
    # black
    elif color == "black":
        # check for color codes
        # if you lost
        if grab() == ColorCodes.lose:
            # decrease money
            decreaseMoney()
            # play double
            print("## [INFO] - Playing again with double ...")
            betBlack(True)
        # if you won
        elif grab() != ColorCodes.lose:
            # increase money
            increaseMoney()
            # play red
            print("## [INFO] - Playing now on red ...")
            betRed(False)

# Set mouse to 'cord' position
def mousePos(cord):
    win32api.SetCursorPos((cord[0], cord[1]))

# Do a left mouse click
def leftClick(cord):
    # debug
    # chip_1
    if (cord == Cord.chip_1):
        print('## [DEBUG] - Clicking on the Chip 1 Euro!')
    # color_red
    elif (cord == Cord.color_red):
        print('## [DEBUG] - Clicking on the Color Red!')
    # color_black
    elif (cord == Cord.color_black):
        print('## [DEBUG] - Clicking on the Color Black!')
    # play
    elif (cord == Cord.play):
        print('## [DEBUG] - Clicking on the Play/Same Amount Button!')
    # double
    elif (cord == Cord.double):
        print('## [DEBUG] - Clicking on the Double Button!')
    # set location
    mousePos((cord))
    time.sleep(.3)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.3)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(.3)

# Start the Game
def gameStart():
    clear()
    # check which casino is setup
    if (Settings.casino == "Bet365"):
        # Bet365
        # check if all settings are set
        if (Settings.money == True and Settings.chip_1 == True and Settings.double == True and Settings.loserSection == True and Settings.redOrBlack != 0 and Settings.start == True and Settings.black == True and Settings.red == True):
            # start game
            time.sleep(.3)
            # click on location chip with number 1€
            leftClick(Cord.chip_1)
            time.sleep(.3)
            if (Settings.redOrBlack == 1):
                # begin with black
                betBlack()
            else:
                # begin with red
                betRed()
        else:
            clear()
            print(hashLine)
            print("## [INFO] - You have not configurated the Bot yet!")
            print(hashLine)
            time.sleep(2)
            menu()
    elif (Settings.casino == "CasinoClub"):
        # CasinoClub
        print('## [INFO] - Money count will be wrong when you get a 0 Color Green, because the Bot can\'t see if you hit Green and receives 0.50 Euro!')
        # check if all settings are set
        if (Settings.money == True and Settings.chip_1 == True and Settings.loserSection == True and Settings.redOrBlack != 0 and Settings.start == True and Settings.black == True and Settings.red == True):
            # start game
            time.sleep(.3)
            # click on location 'play' [Take a sit]
            leftClick(Cord.play)
            time.sleep(.3)
            # click on location 'chip_1'
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
            print("## [INFO] - You have not configurated the Bot yet!")
            time.sleep(2)
            menu()

## MENU MANAGEMENT
# Settings
def menuSettings(key):
    if key == "1":
        clear()
        # change money amount
        print(hashLine)
        print('## Change Money')
        print(hashLine)
        print('## [INFO] - Enter like:')
        print('## [INFO] - 5€ = 5.0')
        print('## [INFO] - 10€ = 10.0')
        print('## [INFO] - 25,50€ = 25.5')
        Settings.money = True
        time.sleep(.1)
        print('##')
        Player.money = float(input('## - Money in your Hand? '))
        settingsInfo()
    elif key == "2":
        clear()
        # save position for roll/start
        print(hashLine)
        print('## Change Start Button')
        print(hashLine)
        print('## [INFO] - Wait for saving position for Play button ...')
        Settings.start = True
        time.sleep(.1)
        saveCords('play')
        settingsInfo()
    elif key == "3":
        clear()
        # save position for double
        print(hashLine)
        print('## Change Double Button')
        print(hashLine)
        print('## [INFO] - Wait for saving position for Double button ...')
        Settings.double = True
        time.sleep(.1)
        saveCords('double')
        settingsInfo()
    elif key == "4":
        clear()
        # save position for color red
        print(hashLine)
        print('## Change Color Red')
        print(hashLine)
        print('## [INFO] - Wait for saving position for Red color ...')
        Settings.red = True
        time.sleep(.1)
        saveCords('color_red')
        settingsInfo()
    elif key == "5":
        clear()
        # save position for color black
        print(hashLine)
        print('## Change Color Black')
        print(hashLine)
        print('## [INFO] - Wait for saving position for Black color ...')
        Settings.black = True
        time.sleep(.1)
        saveCords('color_black')
        settingsInfo()
    elif key == "6":
        clear()
        # save position for chip 1€
        print(hashLine)
        print('## Change Chip 1 Euro')
        print(hashLine)
        print('## [INFO] - Wait for saving position for 1 Euro Chip ...')
        Settings.chip_1 = True
        time.sleep(.1)
        saveCords('chip_1')
        settingsInfo()
    elif key == "7":
        clear()
        # change loser section
        print(hashLine)
        print('## Change Loser Section')
        print(hashLine)
        print('## [INFO] - Wait for saving position for Loser Section ...')
        Settings.loserSection = True
        time.sleep(.1)
        saveCords('loser')
        saveColor = grab()
        ColorCodes.lose = saveColor
        settingsInfo()
    elif key == "8":
        clear()
        # change start by black or red
        print(hashLine)
        print('## Change Black Or Red')
        print(hashLine)
        print('## [INFO] - Choose the starting Bet:')
        print('## [INFO] - Black = 1')
        print('## [INFO] - Red = 2')
        time.sleep(.1)
        print('##')
        Settings.redOrBlack = int(input('## - Start with Black or Red? '))
        settingsInfo()
    elif key == "-1":
        # go back without saving
        time.sleep(.1)
        menu()
    elif key == "0":
        # save config
        time.sleep(.1)
        writeConfig()
    # Error : Try again
    else:
        # wrong key
        time.sleep(.1)
        settingsInfo()

# Casino Selection
def menuCasino(key):
    # Casino Key
    if key == "1":
        # Bet365
        Settings.casino = "Bet365"
        time.sleep(.1)
        settingsInfo()
    elif key == "2":
        # CasinoClub
        Settings.casino = "CasinoClub"
        time.sleep(.1)
        settingsInfo()
    elif key == "0":
        # Select nothing
        time.sleep(.1)
        settingsInfo()
    # Error : Try again
    else:
        # wrong key
        time.sleep(.1)
        casinoInfo()

## MENUS
# Menu
def menu():
    clear()
    print(hashLine)
    print('## ROULETTE BOT MENU')
    print(hashLine)
    time.sleep(.1)
    print('## NAVIGATION OPTION')
    print(hashLine)
    time.sleep(.1)
    print('## [1] - Start Bot')
    print('## [2] - Configurate Bot')
    print('##')
    print('## [9] - Open About')
    print('## [0] - Exit')
    print(hashLine)
    time.sleep(.3)
    # navigate to settings
    menu_nav = input('Select an option [1|2|9|0] and hit ENTER: ')
    # if 1
    if menu_nav == '1':
        # start bot
        gameStart()
    elif menu_nav == '2':
        # start config
        startConfig()
    elif menu_nav == '9':
        # start about
        startAbout()
    elif menu_nav == '0':
        # exit
        exit()
    else:
        # try again
        menu()
# Config
def startConfig():
    clear()
    casinoInfo()
# About
def startAbout():
    clear()
    # about me
    print(hashLine)
    print('## ABOUT ROULETTEBOT')
    print(hashLine)
    print('## Bot was created by SyfuxX!')
    print('## Thank you for using it.')
    time.sleep(.1)
    print(hashLine)
    print('## NAVIGATION OPTION')
    print(hashLine)
    time.sleep(.1)
    print('## [1] - Back to Main Menu')
    print('##')
    print('## [0] - Exit')
    print(hashLine)
    time.sleep(.3)
    # navigate to settings
    menu_nav = input('Select an option [1|0] and hit ENTER: ')
    if menu_nav == '1':
        # start about
        menu()
    if menu_nav == '0':
        # exit
        exit()
# Casino Info
def casinoInfo():
    time.sleep(1)
    # asking for which casino he/she plays
    clear()
    print(hashLine)
    print('## SELECT A CASINO')
    print(hashLine)
    print('## [1] - Bet365')
    print('## [2] - CasinoClub')
    print('##')
    print('## [0] - Skip')
    print(hashLine)
    time.sleep(.1)
    casinoOption = input("Select an option [1|2|0] and hit ENTER: ")
    menuCasino(casinoOption)
# Settings Info
def settingsInfo():
    # asking for the configurations needs
    clear()
    print(hashLine)
    print('## '+ str(Settings.casino))
    print(hashLine)
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
    # Button : Double
    # check if casino is 'Bet365'
    if Settings.casino == "Bet365":
        # check if 'double' is set
        if Settings.double == True:
            print('## [3] - Double Button [X] - '+ str(Cord.double))
        else:
            print('## [3] - Double Button [ ]')
    else:
        print('## [3] - Double Button [AVAILABLE IN BET365 CASINO]')
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
    print('## [-1] - Do not Save Config')
    print('## [0] - Save Config')
    print(hashLine)
    time.sleep(.1)
    option = input("Select an option [1|2|3|4|5|6|7|8|-1|0] and hit ENTER: ")
    menuSettings(option)

## CONFIG FILE
# Set File
def setConfig():
    # Check : If there is a config file
    if os.path.isfile(configName):
        Config.read(configName)
        # Read File and Save to Bot
        # SETTINGS
        Settings.money = Config.getboolean('Settings', 'money')
        Settings.chip_1 = Config.getboolean('Settings', 'chip_1')
        Settings.start = Config.getboolean('Settings', 'start')
        Settings.double = Config.getboolean('Settings', 'double')
        Settings.red = Config.getboolean('Settings', 'red')
        Settings.black = Config.getboolean('Settings', 'black')
        Settings.loserSection = Config.getboolean('Settings', 'loserSection')
        Settings.redOrBlack = Config.getint('Settings', 'redOrBlack')
        Settings.casino = Config.get('Settings', 'casino')
        # PLAYER
        Player.money = Config.getfloat('Player', 'money')
        # CORD
        # chip 1
        cordChip1F = Config.getint('Cord', 'chip_1_f')
        cordChip1S = Config.getint('Cord', 'chip_1_s')
        Cord.chip_1 = (cordChip1F, cordChip1S)
        # color red
        cordRedF = Config.getint('Cord', 'color_red_f')
        cordRedS = Config.getint('Cord', 'color_red_s')
        Cord.color_red = (cordRedF, cordRedS)
        # color black
        cordBlackF = Config.getint('Cord', 'color_black_f')
        cordBlackS = Config.getint('Cord', 'color_black_s')
        Cord.color_black = (cordBlackF, cordBlackS)
        # play
        cordPlayF = Config.getint('Cord', 'play_f')
        cordPlayS = Config.getint('Cord', 'play_s')
        Cord.play = (cordPlayF, cordPlayS)
        # double
        cordDoubleF = Config.getint('Cord', 'double_f')
        cordDoubleS = Config.getint('Cord', 'double_s')
        Cord.double = (cordDoubleF, cordDoubleS)
        # loser
        cordLoserF = Config.getint('Cord', 'loser_f')
        cordLoserS = Config.getint('Cord', 'loser_s')
        cordLoserT = Config.getint('Cord', 'loser_t')
        cordLoserFo = Config.getint('Cord', 'loser_fo')
        Cord.loser = (cordLoserF, cordLoserS, cordLoserT, cordLoserFo)
        time.sleep(1)
        clear()
        print(hashLine)
        print('## WELCOME')
        print(hashLine)
        print('## [INFO] - Loading Config ')
        time.sleep(.5)
        clear()
        print(hashLine)
        print('## WELCOME')
        print(hashLine)
        print('## [INFO] - Loading Config .')
        time.sleep(.5)
        clear()
        print(hashLine)
        print('## WELCOME')
        print(hashLine)
        print('## [INFO] - Loading Config ..')
        time.sleep(.5)
        clear()
        print(hashLine)
        print('## WELCOME')
        print(hashLine)
        print('## [INFO] - Loading Config ...')
        time.sleep(.5)
        clear()
        print(hashLine)
        print('## WELCOME')
        print(hashLine)
        print('## [INFO] - Config Loaded!')
        time.sleep(.5)
        print('## [INFO] - Starting Menu!')
        time.sleep(1)
        # Start Menu
        menu()
    else:
        # No Config file found
        time.sleep(1)
        clear()
        print(hashLine)
        print('## WELCOME')
        print(hashLine)
        print('## [INFO] - Loading Config ')
        time.sleep(.5)
        clear()
        print(hashLine)
        print('## WELCOME')
        print(hashLine)
        print('## [INFO] - Loading Config .')
        time.sleep(.5)
        clear()
        print(hashLine)
        print('## WELCOME')
        print(hashLine)
        print('## [INFO] - Loading Config ..')
        time.sleep(.5)
        clear()
        print(hashLine)
        print('## WELCOME')
        print(hashLine)
        print('## [INFO] - Loading Config ...')
        time.sleep(.5)
        clear()
        print(hashLine)
        print('## WELCOME')
        print(hashLine)
        print('## [ERROR] - No Config File found!')
        time.sleep(.5)
        print('## [INFO] - Starting Menu!')
        time.sleep(1)
        # Start Menu
        menu()

# Write File
def writeConfig():
    # Create the configuration file
    cfg = open(configName, 'w')

    # Add content to config
    # SETTINGS
    if not (Config.has_section('Settings')):
        Config.add_section('Settings')
    Config.set('Settings', 'money', str(Settings.money))
    Config.set('Settings', 'chip_1', str(Settings.chip_1))
    Config.set('Settings', 'start', str(Settings.start))
    Config.set('Settings', 'double', str(Settings.double))
    Config.set('Settings', 'red', str(Settings.red))
    Config.set('Settings', 'black', str(Settings.black))
    Config.set('Settings', 'loserSection', str(Settings.loserSection))
    Config.set('Settings', 'redOrBlack',str( Settings.redOrBlack))
    Config.set('Settings', 'casino', str(Settings.casino))
    # PLAYER
    if not (Config.has_section('Player')):
        Config.add_section('Player')
    Config.set('Player', 'money', str(Player.money))
    # CORD
    if not (Config.has_section('Cord')):
        Config.add_section('Cord')
    Config.set('Cord', 'chip_1_f', str(Cord.chip_1_f))
    Config.set('Cord', 'chip_1_s', str(Cord.chip_1_s))
    Config.set('Cord', 'color_red_f', str(Cord.color_red_f))
    Config.set('Cord', 'color_red_s', str(Cord.color_red_s))
    Config.set('Cord', 'color_black_f', str(Cord.color_black_f))
    Config.set('Cord', 'color_black_s', str(Cord.color_black_s))
    Config.set('Cord', 'play_f', str(Cord.play_f))
    Config.set('Cord', 'play_s', str(Cord.play_s))
    Config.set('Cord', 'double_f', str(Cord.double_f))
    Config.set('Cord', 'double_s', str(Cord.double_s))
    Config.set('Cord', 'loser_f', str(Cord.loser_f))
    Config.set('Cord', 'loser_s', str(Cord.loser_s))
    Config.set('Cord', 'loser_t', str(Cord.loser_t))
    Config.set('Cord', 'loser_fo', str(Cord.loser_fo))
    Config.write(cfg)
    cfg.close()

    clear()
    print(hashLine)
    print('## CONFIG')
    print(hashLine)
    print('## [INFO] - Saving Config ')
    time.sleep(.5)
    clear()
    print(hashLine)
    print('## CONFIG')
    print(hashLine)
    print('## [INFO] - Saving Config .')
    time.sleep(.5)
    clear()
    print(hashLine)
    print('## CONFIG')
    print(hashLine)
    print('## [INFO] - Saving Config ..')
    time.sleep(.5)
    clear()
    print(hashLine)
    print('## CONFIG')
    print(hashLine)
    print('## [INFO] - Saving Config ...')
    time.sleep(.5)
    clear()
    print(hashLine)
    print('## CONFIG')
    print(hashLine)
    print('## [INFO] - Config Saved!')
    time.sleep(.5)
    print('## [INFO] - Going back to Menu!')
    time.sleep(1)
    # Start menu
    menu()

if __name__ == '__main__':
    #getCords()
    #menu()
    setConfig()
    #grab()