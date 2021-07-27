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
import PanedWindow

WIDTH = 500
HEIGHT = 500

class viewerGUI(tk.Frame):
    def __init__(self, root, master=None):
        super().__init__(master)

        # PanedWindowの作成
        self.paned_window = PanedWindow.panedWindow(root)

        self.mainloop()

if __name__ == '__main__':
    root = tk.Tk()
    gui = viewerGUI(root, master=root)
