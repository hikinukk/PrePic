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

        # self.paned_window_list = []

        # PanedWindowの作成
        paned_window = tk.PanedWindow(root, sashwidth = 4)
        paned_window.pack(expand = True, fill = tk.BOTH)

        # Frameの作成
        widget1 = imgFrame.frameGUI(root, WIDTH, HEIGHT)
        widget1.popUpMenu.add_command(label='ウィンドウ分割',underline=5,command=lambda:self.create_paned_frame(paned_window, widget1, root))
        widget1.update()

        # フレームをPanedWindowに追加
        paned_window.add(widget1.app_frame)

        # self.paned_window_list.append(self.paned_window)

    def create_paned_frame(self, parentWindow, widget1, root):
        # PanedWindowの作成
        paned_window2 = tk.PanedWindow(parentWindow, sashwidth = 4)
        paned_window2.pack(expand = True, fill = tk.BOTH)
        
        # 親Frameのサイズを半分にする
        widget1.resize_frame_y()
        # 新しいFrameを作成
        widget2 = imgFrame.frameGUI(root, widget1.winfo_width(), widget1.winfo_height())

        # 新しいFrameの機能を追加
        widget2.popUpMenu.add_command(label='ウィンドウ分割',underline=5,command=lambda:self.create_paned_frame(paned_window2, widget2, root))
        widget2.update()
        
        # FrameをPanedWindowに追加
        paned_window2.add(widget1.app_frame) # 親Frame
        paned_window2.add(widget2.app_frame) # 新しいFrame
        
        # 親PanedWindowに新しいPanedWindowを追加
        parentWindow.add(paned_window2)

        # self.paned_window_list.append(paned_window2)


