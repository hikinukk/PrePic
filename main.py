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



        self.frame = imgFrame.frameGUI(root)
        self.frame2 = imgFrame.frameGUI(root)
        self.frame3 = imgFrame.frameGUI(root)

        self.frame.pack(fill=tk.BOTH, expand=True)
        self.frame2.pack(fill=tk.BOTH, expand=True)
        self.frame3.pack(fill=tk.BOTH, expand=True)

        self.frame.update()
        self.frame2.update()
        self.frame3.update()
        self.mainloop()
        
    def addPage(self, page, name):
        assert not name in self._pages
        self._pages[name] = page
        self._current = name
        page.grid(row=0, column=0, sticky=tk.NSEW)


if __name__ == '__main__':
    root = tk.Tk()
    gui = viewerGUI(root, master=root)
