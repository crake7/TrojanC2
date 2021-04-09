import base64
import win32api
import win32con
import win32gui
import win32ui

def get_dimensions():
    width   = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height  = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left    = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top     = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    return (width, height, left, top)

def screenshot(name='screenshot'):

    # Learn more here: https://docs.microsoft.com/en-us/windows/win32/gdi/device-contexts.
     
    # Get a handle for the entire desktop
    hdesktop = win32gui.GetDesktopWindow()
    width, height, left, top = get_dimensions()

    # Create a device context
    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc     = win32ui.CreateDCFromHandle(desktop_dc)
    # Create a memory-based device context to store the images until we write it the bitmap bytes to a file
    mem_dc     = img_dc.CreateCompatibleDC()

    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(img_dc, width, height)
    # Sets the memory-based dc to point at the bitmap object captured
    mem_dc.SelectObject(screenshot)
    # Make bit-for-bit copy of desktop image and sotre it in mem_dc
    mem_dc.BitBlt((0,0), (width, height), img_dc, (left, top), win32con.SRCCOPY)
    screenshot.SaveBitmapFile(mem_dc, f'{name}.bmp')

    mem_dc.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())

def run():
    screenshot()
    with open('screenshot.bmp') as f:
        img=f.read()
        return img

if __name__ == '__main__':
    screenshot()
