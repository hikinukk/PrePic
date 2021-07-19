# coding: utf-8

import cv2
import numpy as np
from PIL import ImageGrab
from PIL import Image, ImageTk
import ctypes
import ctypes.wintypes
import time

import tkinter as tk
import tkinter.ttk as ttk
import threading
import mss
import sys

import imgFrame

WIDTH = 500
HEIGHT = 500

class viewerGUI(tk.Frame):
    def __init__(self, root, master=None):
        super().__init__(master)


        # PanedWindowの作成
        self.paned_window = tk.PanedWindow(self.master, sashwidth = 4)

        # Frameの作成
        self.widget1 = imgFrame.frameGUI(root)
        self.widget2 = imgFrame.frameGUI(root)

        # フレームをPanedWindowに追加
        self.paned_window.add(self.widget1.app_frame)
        self.paned_window.add(self.widget2.app_frame)

        self.paned_window.pack(expand = True, fill = tk.BOTH)

        self.widget1.update()
        self.widget2.update()

        self.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    gui = viewerGUI(root, master=root)
