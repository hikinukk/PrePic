# coding: utf-8

import cv2
import numpy as np
from PIL import ImageGrab
from PIL import Image, ImageTk
import ctypes
import ctypes.wintypes
import time

import tkinter as tk
import threading
import mss
import sys

WIDTH = 800
HEIGHT = 500

class viewerGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.create_canvas()
        self.create_popupmenu()
        self.create_key_handler()
        
        self.update()
        self.mainloop()

    # ----------------------画像表示canvas設定----------------------
    def create_canvas(self):
        # canvas作成
        fm_upper = tk.Frame(self.master)
        fm_upper.pack(fill=tk.X, side=tk.TOP)
        self.canvas = tk.Canvas(fm_upper, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

    # 画像を更新する処理
    def update_canvas(self):
        self.window_size = viewerGUI.GetWindowRectFromName("無題 - メモ帳")

        # 画像読み込み(mssとImageGrabどっちがいいのかまだわかってない)
        self.grab_image = mss.mss().grab(self.window_size)
        # self.grab_image = ImageGrab.grab(self.window_size)
        # 配列に変換
        self.cv_img = np.array(self.grab_image)
        # 色変換
        self.cv_img= cv2.cvtColor(self.cv_img, cv2.COLOR_RGB2BGR)
        # canvasに画像を表示
        self.im = ImageTk.PhotoImage(image=Image.fromarray(self.cv_img))
        self.canvas.create_image(0, 0, image=self.im, anchor='nw')

    def update(self):
        self.update_canvas()
        self.after(15,self.update)

    # ----------------------キー入力設定----------------------
    def key_handler(self, event):
        print(event.keycode)

    def create_key_handler(self):
        root.bind("<KeyPress>", self.key_handler)

    # ----------------------ポップアップメニューの設定----------------------
    def show_popupmenu(self, event):
        self.popUpMenu.post(event.x_root, event.y_root)

    def create_popupmenu(self):
        # ポップアップメニューの設定
        self.popUpMenu = tk.Menu(
            root,
            tearoff = False, # tearoff=False:指定しないとメニューがきりとられちゃう
        )
        # [ポップアップメニュー] - [Command-1]
        self.popUpMenu.add_command(
            label = "終了",
            command=self.command_1
        )
        # 右クリックイベント関連付け
        root.bind("<Button-3>", self.show_popupmenu)

    # Command1処理
    def command_1(self):
        print("終了")
        sys.exit()

    # ----------------------ウィンドウハンドラ----------------------
    # ウィンドウの名前からウィンドウの位置を取得
    def GetWindowRectFromName(TargetWindowTitle:str)-> tuple:
        TargetWindowHandle = ctypes.windll.user32.FindWindowW(0, TargetWindowTitle)
        Rectangle = ctypes.wintypes.RECT()
        ctypes.windll.user32.GetWindowRect(TargetWindowHandle, ctypes.pointer(Rectangle))
        return (Rectangle.left, Rectangle.top, Rectangle.right, Rectangle.bottom)



if __name__ == '__main__':
    root = tk.Tk()
    gui = viewerGUI(master=root)
