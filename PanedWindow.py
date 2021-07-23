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

        # self.panedWindow_list = []

        # 親PanedWindowの作成
        parentWindow = ttk.PanedWindow(root, orient = 'horizontal') 
        parentWindow.pack(expand = True, fill = tk.BOTH)

        # PanedWindowの作成
        panedWindow = ttk.PanedWindow(root, orient = 'horizontal')
        # panedWindow.pack(expand = True, fill = tk.BOTH)
        parentWindow.add(panedWindow)

        # Frameの作成
        frameWidget = imgFrame.frameGUI(root, WIDTH, HEIGHT)
        frameWidget.popUpMenu.add_command(label='ウィンドウを縦に分割',underline=5,command=lambda:self.create_paned_frame(panedWindow, frameWidget, "|", root))
        frameWidget.popUpMenu.add_command(label='ウィンドウを横に分割',underline=5,command=lambda:self.create_paned_frame(panedWindow, frameWidget, "-", root))
        frameWidget.update()

        # フレームをPanedWindowに追加
        panedWindow.add(frameWidget.app_frame)

        # self.panedWindow_list.append(self.panedWindow)

    def create_paned_frame(self, parentPanedWindow, parentFrameWidget, direction, root):
        # PanedWindowの作成
        if direction == "|":
            panedWindow = ttk.PanedWindow(parentPanedWindow, orient = 'horizontal') # 垂直方向のpanedWindowを作成
            parentFrameWidget.resize_frame_y() # 親Frameの横サイズを半分にする
        elif direction == "-":
            panedWindow = ttk.PanedWindow(parentPanedWindow, orient = 'vertical') # 平行方向のpanedWindowを作成
            parentFrameWidget.resize_frame_x() # 親Frameの縦サイズを半分にする

        print(parentFrameWidget.app_frame,"::",type(parentFrameWidget.app_frame))

        # 親PanedWindowに新しいPanedWindowを追加
        parentPanedWindow.add(panedWindow)
        
        # 新しいFrameを作成
        frameWidget = imgFrame.frameGUI(root, parentFrameWidget.winfo_width(), parentFrameWidget.winfo_height())

        # 新しいFrameの機能を追加
        frameWidget.popUpMenu.add_command(label='ウィンドウを縦に分割',underline=5,command=lambda:self.create_paned_frame(panedWindow, frameWidget, "|", root))
        frameWidget.popUpMenu.add_command(label='ウィンドウを横に分割',underline=5,command=lambda:self.create_paned_frame(panedWindow, frameWidget, "-", root))
        frameWidget.update()


        # FrameをPanedWindowに追加
        panedWindow.add(parentFrameWidget.app_frame) # 親Frame
        panedWindow.add(frameWidget.app_frame) # 新しいFrame
        


