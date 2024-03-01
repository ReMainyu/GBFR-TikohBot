import pydirectinput
from pynput import keyboard
from pynput.keyboard import Listener
import time
import threading

is_active = False
pydirectinput.FAILSAFE = False

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
            moveToQuestCounter()
    
def autofire():
    '''Press and hold left click in accordance to Rackam's perfect primary attack timing'''
    while is_active:
        pydirectinput.mouseDown()
        time.sleep(0.55)
        pydirectinput.mouseUp()

def pickLocation():
    pass

def moveToQuestCounter():
    pydirectinput.press("r")
    pydirectinput.press("enter")
    pydirectinput.press("enter")
    pydirectinput.keyDown("w")
    time.sleep(1.1)
    pydirectinput.keyUp("w")
    pydirectinput.press("f")

def basicSlimeBlasting():
    '''Moves into postion for slime blasting'''
    pydirectinput.keyDown("w")
    time.sleep(6.25)
    pydirectinput.keyUp("w")

    autofire()

with Listener(on_press=on_press) as listener:
    try:
        listener.join()
    except Exception as e:
        print('{0} was pressed'.format(e.args[0]))