import psutil
import win32gui, win32ui, win32con, win32api, win32process
import cv2
import numpy as np
from ctypes import windll

class InfoGrabber():
    def __init__(self, process):
        self._pid = 0
        self._hwnd = 0
        self._windows = []
        self._process = process

        # The name is the same as the process
        self._name = process.replace(".exe", "")

        # Return a list of processes with the name
        ls = []
        for p in psutil.process_iter(attrs=['name']):
            if p.info['name'] == process:
                ls.append(p)

        self._pid = ls[0].pid

        win32gui.EnumWindows(self._enum_window_callback, self._pid)

        # There should only be one window
        self._hwnd = self._windows[0]

        windll.user32.SetProcessDPIAware()

    def _enum_window_callback(self, hwnd, pid):
        _, current_pid = win32process.GetWindowThreadProcessId(hwnd)
        if pid == current_pid and win32gui.IsWindowVisible(hwnd):
            self._windows.append(hwnd)

    def get_pid(self):
        return self._pid

    def get_hwnd(self):
        return self._hwnd

    def np_screenshot(self, width, height):
        # Get the screenshot
        img = self.screenshot(width, height)

        # Convert to numpy array
        img = np.array(img)

        # Expand to third dimension for convolution
        img = np.expand_dims(img, 3)

        return img

    def screenshot(self, res_width, res_height):
        # Set the current window to your window
        win32gui.SetForegroundWindow(self._hwnd)

        # Credits to Frannecklp
        hwin = win32gui.GetWindow(self._hwnd, win32con.GW_OWNER) 
    
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    
        hwindc = win32gui.GetWindowDC(hwin)
        srcdc = win32ui.CreateDCFromHandle(hwindc)
        memdc = srcdc.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(srcdc, width, height)
        memdc.SelectObject(bmp)
        memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
        
        signedIntsArray = bmp.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (height,width,4)
    
        srcdc.DeleteDC()
        memdc.DeleteDC()
        win32gui.ReleaseDC(hwin, hwindc)
        win32gui.DeleteObject(bmp.GetHandle())
    
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (res_width, res_height))
    
        return img
