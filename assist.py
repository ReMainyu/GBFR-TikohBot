#!/usr/bin/env python
__author__      = "ReMainyu"

import time
import threading
from enum import Enum
from random import randint

import pydirectinput
from pynput import keyboard
from pynput.keyboard import Listener

is_active = False
pydirectinput.FAILSAFE = False

class POI(Enum):
    QUEST_COUNTER = 0
    BLACKSMITH = 1
    SIERO = 2
    ZATHBA = 3
    DOCKS = 4

def on_press(key):
    global is_active
    match key:
        case keyboard.Key.f1:
            is_active = not is_active
            if is_active:
                thread = threading.Thread(target=autofire)
                thread.start()
        case keyboard.Key.f2:
            is_active = not is_active
            if is_active:
                thread = threading.Thread(target=basicSlimeBlasting)
                thread.start()
        case keyboard.Key.f3:
            moveToPOI(0)
        case keyboard.Key.f5:
            exit()
    
def autofire():
    '''Press and hold left click in accordance to Rackam's perfect primary attack timing'''
    while is_active:
        pydirectinput.mouseDown()
        time.sleep(0.55)
        pydirectinput.mouseUp()

def moveToPOI(order):
    pydirectinput.press("r")
    pydirectinput.press("enter")
    for i in range(order):
        pydirectinput.press("down")
    pydirectinput.press("enter")

    pydirectinput.keyDown("w")
    time.sleep(1.4)
    pydirectinput.keyUp("w")
    pydirectinput.press("f")

def basicSlimeBlasting():
    '''Selects and move into postion for slime blasting'''
    location = randint(0, 3)
    print(location)
    match location:
        case 1:
            pydirectinput.keyDown("w")
            time.sleep(6.25)
            pydirectinput.keyUp("w")
        case 2:
            pydirectinput.keyDown("w")
            time.sleep(2.8)
            pydirectinput.keyDown("a")
            time.sleep(2.1)
            pydirectinput.keyUp("w")
            pydirectinput.keyUp("a")
        case 3:
            pydirectinput.keyDown("w")
            time.sleep(2.8)
            pydirectinput.keyDown("d")
            time.sleep(2.1)
            pydirectinput.keyUp("w")
            pydirectinput.keyUp("d")
        case _:
            pass

    autofire()

with Listener(on_press=on_press) as listener:
    try:
        listener.join()
    except Exception as e:
        print('{0} was pressed'.format(e.args[0]))