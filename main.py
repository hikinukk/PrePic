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

WIDTH = 500
HEIGHT = 500

class viewerGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.color_filter = "default"
        self.is_image_flip_horizontal = False
        self.is_image_flip_upside_down =False

        self.create_canvas()
        self.create_popupmenu()
        self.create_key_handler()
        
        self.update()
        self.mainloop()

    # ----------------------画像表示canvas設定----------------------
    def create_canvas(self):
        fm_upper = tk.Frame(self.master)
        fm_upper.pack(fill=tk.BOTH, expand=1)
        # canvas作成
        self.canvas = tk.Canvas(fm_upper, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=tk.BOTH, expand=1)

    # 画像を更新する処理
    def update_canvas(self):
        self.window_size = viewerGUI.GetWindowRectFromName("無題 - メモ帳")

        # 画像読み込み(mssとImageGrabどっちがいいのかまだわかってない)
        self.grab_image = mss.mss().grab(self.window_size)
        # self.grab_image = ImageGrab.grab(self.window_size)
        # 配列に変換
        self.cv_img = np.array(self.grab_image)
        # 色変換
        if self.color_filter == "default":
            self.cv_img= cv2.cvtColor(self.cv_img, cv2.COLOR_RGB2BGR)
        elif self.color_filter == "gray":
            self.cv_img= cv2.cvtColor(self.cv_img, cv2.COLOR_BGR2GRAY)
        elif self.color_filter == "inversion":
            self.cv_img= cv2.cvtColor(self.cv_img, cv2.COLOR_RGB2BGR)
            self.cv_img = cv2.bitwise_not(self.cv_img)
        # 画像編集
        if self.is_image_flip_horizontal:
            self.cv_img = cv2.flip(self.cv_img, 1)
        if self.is_image_flip_upside_down:
            self.cv_img = cv2.flip(self.cv_img, 0)

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
        self.popUpMenu = tk.Menu(root, tearoff = False)
        self.popUpMenu_filter = tk.Menu(self.popUpMenu, tearoff = False)
        self.popUpMenu_flip = tk.Menu(self.popUpMenu, tearoff = False)

        # [ポップアップメニュー] - [Command]
        self.popUpMenu.add_cascade(label='フィルタ',menu=self.popUpMenu_filter,under=5)
        self.popUpMenu_filter.add_command(label='デフォルト',underline=5,command=self.command_filter_default)
        self.popUpMenu_filter.add_command(label='グレースケール',underline=5,command=self.command_filter_gray)
        self.popUpMenu_filter.add_command(label='色反転',underline=5,command=self.command_filter_color_inversion)

        self.popUpMenu.add_cascade(label='画面表示',menu=self.popUpMenu_flip,under=5)
        self.popUpMenu_flip.add_command(label='デフォルト',underline=5,command=self.command_flip_default)
        self.popUpMenu_flip.add_command(label='左右反転',underline=5,command=self.command_flip_horizontal)
        self.popUpMenu_flip.add_command(label='上下反転',underline=5,command=self.command_flip_upside_down)

        self.popUpMenu.add_command(label = "終了", command=self.command_finish)


        # 右クリックイベント関連付け
        root.bind("<Button-3>", self.show_popupmenu)

    # Command処理
    def command_filter_default(self): # bデフォルト
        self.color_filter = "default"
    def command_filter_gray(self): # グレースケール
        self.color_filter = "gray"
    def command_filter_color_inversion(self): # 色反転
        self.color_filter = "inversion"

    def command_flip_default(self): # デフォルト
        self.is_image_flip_horizontal = False
        self.is_image_flip_upside_down = False
    def command_flip_horizontal(self): # 左右反転
        if not self.is_image_flip_horizontal:
            self.is_image_flip_horizontal = True
        else:
            self.is_image_flip_horizontal = False
    def command_flip_upside_down(self): # 上下反転
        if not self.is_image_flip_upside_down:
            self.is_image_flip_upside_down = True
        else:
            self.is_image_flip_upside_down = False

    def command_finish(self):
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
