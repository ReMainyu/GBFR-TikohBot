#!/usr/bin/env python
__author__      = 'ReMainyu'

import time
import threading
from enum import Enum
from random import randint

from pymem import *
from pymem.ptypes import RemotePointer
import pydirectinput
from pynput.keyboard import Key, HotKey, Listener

pydirectinput.FAILSAFE = False
pydirectinput.PAUSE = 0.05

class TOWN_SHORTCUTS(Enum):
    QUEST_COUNTER = 0
    BLACKSMITH = 1
    SIERO = 2
    ZATHBA = 3
    DOCKS = 4

class Assist:
    def __init__(self):
        self.mem = pymem.Pymem('granblue_fantasy_relink.exe')
        self.is_active = False
        self.HOTKEYS = [
            HotKey(HotKey.parse('<ctrl>+q'), exit),
            HotKey(HotKey.parse('r+1'), lambda: self.move_to_POI(TOWN_SHORTCUTS.QUEST_COUNTER.value)),
            HotKey(HotKey.parse('r+2'), lambda: self.move_to_POI(TOWN_SHORTCUTS.BLACKSMITH.value)),
            HotKey(HotKey.parse('r+3'), lambda: self.move_to_POI(TOWN_SHORTCUTS.SIERO.value)),
            HotKey(HotKey.parse('r+4'), lambda: self.move_to_POI(TOWN_SHORTCUTS.ZATHBA.value))]

    def autofire(self):
        '''Press and hold left click in accordance to Rackam's perfect primary attack timing'''
        while self.is_active:
            pydirectinput.mouseDown()
            time.sleep(0.6)
            pydirectinput.mouseUp()

    def basic_slimeblast(self):
        '''Selects and move into postion for slime blasting'''
        location = randint(0, 3)
        match location:
            case 1:
                pydirectinput.keyDown('w')
                time.sleep(6.25)
                pydirectinput.keyUp('w')
            case 2:
                pydirectinput.keyDown('w')
                time.sleep(2.9)
                pydirectinput.keyDown('a')
                time.sleep(2.2)
                pydirectinput.keyUp('w')
                pydirectinput.keyUp('a')
            case 3:
                pydirectinput.keyDown('w')
                time.sleep(2.9)
                pydirectinput.keyDown('d')
                time.sleep(2.2)
                pydirectinput.keyUp('w')
                pydirectinput.keyUp('d')
            case _:
                pass

        self.autofire()
        
    def move_to_POI(self, repeat):
        pydirectinput.press('r')
        pydirectinput.press('enter')
        pydirectinput.press('down', presses=repeat, interval=0.1)
        pydirectinput.press('enter')
        pydirectinput.keyDown('w')
        time.sleep(1.6)
        pydirectinput.keyUp('w')
        pydirectinput.press('f')

    def auto_transmute(self):
        while self.is_active:
            pydirectinput.press('enter')
    
    def queue_slimepede(self):
        pydirectinput.press('e')
        pydirectinput.press('up')
        pydirectinput.press('enter')
        pydirectinput.press('q')
        pydirectinput.press('enter')
        pydirectinput.press('enter')
        pydirectinput.press('enter')
        time.sleep(2.5)
        pydirectinput.press('3')
        pydirectinput.press('enter')

    def get_pointer_address(self,base, offsets):
        remote_pointer = RemotePointer(self.mem.process_handle, base)
        for offset in offsets:
            if offset != offsets[-1]:
                remote_pointer = RemotePointer(self.mem.process_handle, remote_pointer.value + offset)
            else:
                return remote_pointer.value + offset
        
    def reset_quest_counter(self):
        offsets = [0x4A0]
        self.mem.write_int(self.get_pointer_address(self.mem.base_address + 0x06772160, offsets), 1)

    def on_press(self, key):
        match key:
            case Key.f1:
                self.is_active = not self.is_active
                if self.is_active:
                    thread = threading.Thread(target=self.autofire)
                    thread.start()
            case Key.f2:
                self.is_active = not self.is_active
                if self.is_active:
                    thread = threading.Thread(target=self.basic_slimeblast)
                    thread.start()
            case Key.f3:
                self.is_active = not self.is_active
                if self.is_active:
                    thread = threading.Thread(target=self.queue_slimepede)
                    thread.start()
            case Key.f6:
                self.is_active = not self.is_active
                if self.is_active:
                    thread = threading.Thread(target=self.auto_transmute)
                    thread.start()
            case Key.f7:
                self.reset_quest_counter()
            case _:
                for hotkey in self.HOTKEYS:
                    hotkey.press(listener.canonical(key))
            
    def on_release(self, key):
        for hotkey in self.HOTKEYS:
            hotkey.release(listener.canonical(key))

if __name__ == '__main__':
    assist = Assist()

    with Listener(on_press=assist.on_press,
                  on_release=assist.on_release) as listener:
        try:
            listener.join()
        except Exception as e:
            print('{0} was pressed'.format(e.args[0]))