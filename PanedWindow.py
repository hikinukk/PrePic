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

class panedWindow(tk.Frame):
    def __init__(self, root ,master=None ):
        super().__init__(master)

        self.paned_window_list = []

        # PanedWindowの作成
        self.paned_window = tk.PanedWindow(root, sashwidth = 4)

        # Frameの作成
        self.widget1 = imgFrame.frameGUI(root)

        # フレームをPanedWindowに追加
        self.paned_window.add(self.widget1.app_frame)

        self.paned_window.pack(expand = True, fill = tk.BOTH)

        # 右クリックメニュー追加
        self.widget1.popUpMenu.add_command(label='ウィンドウ分割',underline=5,command=lambda:self.create_paned_frame(root))

        self.paned_window_list.append(self.paned_window)

        self.widget1.update()

        # self.mainloop()
    def create_paned_frame(self, root):
        print("root")
        # PanedWindowの作成
        paned_window2 = tk.PanedWindow(self.paned_window, sashwidth = 4)
        
        # Frameの作成
        # self.widget1 = self.widget1
        self.widget2 = imgFrame.frameGUI(root)

        # 右クリックメニュー追加
        self.widget2.popUpMenu.add_command(label='ウィンドウ分割',underline=5,command=lambda:self.create_paned_frame(root))
        
        # フレームをPanedWindowに追加
        paned_window2.add(self.widget1.app_frame)
        paned_window2.add(self.widget2.app_frame)
        self.widget2.update()

        # 親PanedWindowにPanedWindowを追加
        self.paned_window.add(paned_window2)

        paned_window2.pack(expand = True, fill = tk.BOTH)

        # self.paned_window_list.append(paned_window2)
        self.widget2.update()

        self.paned_window.pack(expand = True, fill = tk.BOTH)

