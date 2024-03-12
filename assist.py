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

QUEST_TIMER_OFFSETS = [0x1D0, 0x34]
CHEST_TIMER_OFFSETS = [0x1D0, 0x4F4]
RESULT_TIMER_OFFSETS = [0x2C8, 0x60, 0x70, 0x0, 0x88]
REPEAT_COUNTER_OFFSETS = [0x4A0]
VOUCHER_OFFSETS = [0x48, 0x28, 0x28, 0x0, 0x20, 0x38, 0x4]
TRANSMARVEL_OFFSETS = [0x34]
SHORTCUTS_OFFSETS = [0x150, 0x10, 0x10, 0x88, 0x0, 0x294]
FAST_TRAVEL_OFFSETS = [0x2B8, 0x0, 0x28, 0x18, 0x2E4]
CHOICE_OFFSETS = [0x2B0, 0x8, 0x70, 0x8, 0x294]
QUEST_SORTING_OFFSETS = [0x2C8, 0x30, 0x88, 0x0, 0x294]
QUEST_DIFFICULTY_SWAP_OFFSETS = [0x298, 0x60, 0x140, 0x28, 0x38, 0x180]

class TOWN_SHORTCUTS(Enum):
    QUEST_COUNTER = 0
    BLACKSMITH = 1
    SIERO = 2
    ZATHBA = 3
    DOCKS = 4

class Assist:
    def __init__(self):
        try:
            self.mem = pymem.Pymem('granblue_fantasy_relink.exe')
        except:
            exit()
        
        self.is_active = False
        self.enable_skip = False
        self.enable_quest_repeat = False

        self.HOTKEYS = [
            HotKey(HotKey.parse('<ctrl>+q'), exit),
            HotKey(HotKey.parse('r+1'), lambda: self.move_to_POI(TOWN_SHORTCUTS.QUEST_COUNTER.value)),
            HotKey(HotKey.parse('r+2'), lambda: self.move_to_POI(TOWN_SHORTCUTS.BLACKSMITH.value)),
            HotKey(HotKey.parse('r+3'), lambda: self.move_to_POI(TOWN_SHORTCUTS.SIERO.value)),
            HotKey(HotKey.parse('r+4'), lambda: self.move_to_POI(TOWN_SHORTCUTS.ZATHBA.value))]

    def autofire(self):
        '''Press and hold left click in accordance to Rackam's perfect primary attack timing.'''
        while self.is_active:
            pydirectinput.mouseDown()
            time.sleep(0.6)
            pydirectinput.mouseUp()

    def basic_slimeblast(self, location=None):
        '''Selects and move into postion for slime blasting.'''
        if location == None:
            location = randint(0, 3)

        match location:
            case 0:
                pydirectinput.keyDown('w')
                time.sleep(6.25)
                pydirectinput.keyUp('w')
            case 1:
                pydirectinput.keyDown('w')
                time.sleep(2.9)
                pydirectinput.keyDown('a')
                time.sleep(2.2)
                pydirectinput.keyUp('w')
                pydirectinput.keyUp('a')
            case 2:
                pydirectinput.keyDown('w')
                time.sleep(2.9)
                pydirectinput.keyDown('d')
                time.sleep(2.2)
                pydirectinput.keyUp('w')
                pydirectinput.keyUp('d')
            case _:
                pydirectinput.keyDown('w')
                time.sleep(2.2)
                pydirectinput.keyUp('w')

        self.autofire()
    
    def move_to_POI(self, choice):
        '''Uses the in-game fast travel to get to the POI, move towards it and use the interact key.'''
        pydirectinput.press('r')
        # Reset shortcut choice
        self.mem.write_int(self.get_pointer_address(self.mem.base_address + 0x066024A0, SHORTCUTS_OFFSETS), 0)
        pydirectinput.press('enter')
        # Slight delay to let the reset happen before the change
        time.sleep(0.1)
        self.mem.write_int(self.get_pointer_address(self.mem.base_address + 0x067323B8, FAST_TRAVEL_OFFSETS), choice)
        pydirectinput.press('enter')
        pydirectinput.keyDown('w')
        time.sleep(1.6)
        pydirectinput.keyUp('w')
        pydirectinput.press('f')

    def queue_slimepede(self):
        '''Upon interacting with the quest counter, call this to select Slimepede and begin the mission.'''
        pydirectinput.press('enter')
        
        time.sleep(1)

        try:
            choice = self.mem.read_int(self.get_pointer_address(self.mem.base_address + 0x067323B8, QUEST_SORTING_OFFSETS))
            if choice >= 0 and choice < 3:
                self.mem.write_int(self.get_pointer_address(self.mem.base_address + 0x067323B8, QUEST_SORTING_OFFSETS), 1)

            time.sleep(0.1)
            choice = self.mem.read_int(self.get_pointer_address(self.mem.base_address + 0x067323B8, CHOICE_OFFSETS))
            if choice >= 0 and choice < 3:
                self.mem.write_int(self.get_pointer_address(self.mem.base_address + 0x067323B8, CHOICE_OFFSETS), 2)
                pydirectinput.press('enter')

            time.sleep(0.1)
            choice = self.mem.read_int(self.get_pointer_address(self.mem.base_address + 0x067323B8, QUEST_DIFFICULTY_SWAP_OFFSETS))
            if choice == 0 or choice == 1:
                self.mem.write_int(self.get_pointer_address(self.mem.base_address + 0x067323B8, QUEST_DIFFICULTY_SWAP_OFFSETS), 1)
                pydirectinput.press('q')
                pydirectinput.press('enter', presses=6, interval=0.05)
                time.sleep(1.7)
                pydirectinput.press('3')
                pydirectinput.press('enter')
        except:
            pass

    def auto_transmute(self):
        '''Mashes the enter key and stops when vouchers is insufficient.'''
        while self.is_active:
            try:
                choice = self.mem.read_int(self.get_pointer_address(self.mem.base_address + 0x067323B8, CHOICE_OFFSETS))
                print('lvl ', choice)
                if choice == 2:
                    vouchers = self.mem.read_int(self.get_pointer_address(self.mem.base_address + 0x05CF3FF8, VOUCHER_OFFSETS))
                    print(vouchers)
                    if vouchers > 24:
                        pydirectinput.press('enter')
            except:
                pass
    
    def full_auto_slimepede(self):
        self.move_to_POI(0)
        time.sleep(1.5)
        self.queue_slimepede()

        while self.is_active:
            try:
                chest_timer_ptr_value = self.mem.read_float(self.get_pointer_address(self.mem.base_address + 0x05CEC108, QUEST_TIMER_OFFSETS))
                if chest_timer_ptr_value > 178 and chest_timer_ptr_value < 180:
                    threading.Thread(target=lambda: self.basic_slimeblast(0)).start()
                    time.sleep(180)
                    self.is_active = False
                    time.sleep(33)
                    self.is_active = True

            except:
                pass

    def get_pointer_address(self, base, offsets):
        remote_pointer = RemotePointer(self.mem.process_handle, base)
        for offset in offsets:
            if offset != offsets[-1]:
                remote_pointer = RemotePointer(self.mem.process_handle, remote_pointer.value + offset)
            else:
                return remote_pointer.value + offset

    def polling_for_rewards(self):
        '''Continue polling for timer values and flags and react accordingly.'''
        while True:
            try:
                chest_timer = self.mem.read_float(self.get_pointer_address(self.mem.base_address + 0x05CEC108, CHEST_TIMER_OFFSETS))
                result_timer = self.mem.read_float(self.get_pointer_address(self.mem.base_address + 0x067323B8, RESULT_TIMER_OFFSETS))

                if chest_timer > 10:
                    if self.enable_skip:
                        self.mem.write_float(self.get_pointer_address(self.mem.base_address + 0x05CEC108, CHEST_TIMER_OFFSETS), 0.0)

                    if self.enable_quest_repeat:
                        print(self.mem.read_int(self.get_pointer_address(self.mem.base_address + 0x06772160, REPEAT_COUNTER_OFFSETS)))
                        self.mem.write_int(self.get_pointer_address(self.mem.base_address + 0x06772160, REPEAT_COUNTER_OFFSETS), 8)

                if result_timer > 28 and result_timer < 35:
                    if self.enable_skip:
                        self.mem.write_float(self.get_pointer_address(self.mem.base_address + 0x067323B8, RESULT_TIMER_OFFSETS), 5.0)
                    
            except:
                pass

    def on_press(self, key):
        match key:
            case Key.f1:
                self.is_active = not self.is_active
                if self.is_active:
                    threading.Thread(target=self.autofire).start()
            case Key.f2:
                self.is_active = not self.is_active
                if self.is_active:
                    threading.Thread(target=self.basic_slimeblast).start()
            case Key.f3:
                self.is_active = not self.is_active
                if self.is_active:
                    threading.Thread(target=self.full_auto_slimepede).start()
            case Key.f4:
                self.is_active = not self.is_active
                if self.is_active:
                    threading.Thread(target=self.auto_transmute).start()
            case Key.f5:
                self.enable_skip = not self.enable_skip
            case Key.f6:
                self.enable_quest_repeat = not self.enable_quest_repeat
            case _:
                for hotkey in self.HOTKEYS:
                    hotkey.press(listener.canonical(key))
            
    def on_release(self, key):
        for hotkey in self.HOTKEYS:
            hotkey.release(listener.canonical(key))

if __name__ == '__main__':
    assist = Assist()
    thread = threading.Thread(target=assist.polling_for_rewards)
    thread.start()

    with Listener(on_press=assist.on_press,
                  on_release=assist.on_release) as listener:
        try:
            listener.join()
        except:
            pass