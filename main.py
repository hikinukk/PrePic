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
        self.focus_window_name = ""
        self.window_name_list = self.window_title_delete_null(self.get_window_title())

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

        # focusしているウィンドウがなかったらcanvasをクリア
        if self.focus_window_name == "": return

        self.window_size = viewerGUI.GetWindowRectFromName(self.focus_window_name)
        # 画像読み込み(mssとImageGrabどっちがいいのかまだわかってない)
        self.grab_image = mss.mss().grab(self.window_size)
        # self.grab_image = ImageGrab.grab(self.window_size)

        if self.grab_image.width == 0 and self.grab_image.height == 0 :
            self.canvas.delete("all")
            return

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
        self.update_command_window_name()
        self.popUpMenu.post(event.x_root, event.y_root)

    def create_popupmenu(self):
        # ポップアップメニューの設定
        self.popUpMenu = tk.Menu(root, tearoff = False)
        self.popUpMenu_filter = tk.Menu(self.popUpMenu, tearoff = False)
        self.popUpMenu_flip = tk.Menu(self.popUpMenu, tearoff = False)
        self.popUpMenu_window = tk.Menu(self.popUpMenu, tearoff = False)

        # [ポップアップメニュー] - [Command]
        self.popUpMenu.add_cascade(label='フィルタ',menu=self.popUpMenu_filter,under=5)
        self.popUpMenu_filter.add_command(label='デフォルト',underline=5,command=self.command_filter_default)
        self.popUpMenu_filter.add_command(label='グレースケール',underline=5,command=self.command_filter_gray)
        self.popUpMenu_filter.add_command(label='色反転',underline=5,command=self.command_filter_color_inversion)

        self.popUpMenu.add_cascade(label='画面表示',menu=self.popUpMenu_flip,under=5)
        self.popUpMenu_flip.add_command(label='デフォルト',underline=5,command=self.command_flip_default)
        self.popUpMenu_flip.add_command(label='左右反転',underline=5,command=self.command_flip_horizontal)
        self.popUpMenu_flip.add_command(label='上下反転',underline=5,command=self.command_flip_upside_down)

        self.popUpMenu.add_cascade(label='ウィンドウ切り替え', menu=self.popUpMenu_window)
        for window_name in self.window_name_list:
            self.popUpMenu_window.add_command(label=window_name, command= lambda window_name = window_name: self.command_window_change(window_name))

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

    def command_window_change(self, name):
        self.focus_window_name = name

    def command_finish(self):
        print("終了")
        sys.exit()

    # ----------------------ウィンドウハンドラ----------------------
    # ウィンドウ一覧の名前を取得
    def get_window_title(self):
        # コールバック関数を定義(定義のみで実行ではない) コールバック関数はctypes.WINFUNCTYPEで作成可能
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
        # 開いているウィンドウ一覧を取得
        EnumWindows = ctypes.windll.user32.EnumWindows
        # タイトル格納用変数
        title = []

        def foreach_window(hwnd, lparam):
            if ctypes.windll.user32.IsWindowVisible(hwnd): # ウィンドウが表示されているかどうか
                length = ctypes.windll.user32.GetWindowTextLengthW(hwnd) # タイトルバー取得
                buff = ctypes.create_unicode_buffer(length +1)
                ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
                title.append(buff.value)

                return True

        EnumWindows(EnumWindowsProc(foreach_window), 0)
        
        return title

    # get_window_titleで取得したウィンドウ一覧には空の名前が含まれているため取り除く
    def window_title_delete_null(self, window_name_list):
        return [name for name in window_name_list if name != '']

    # ウィンドウの名前からウィンドウの位置を取得
    def GetWindowRectFromName(TargetWindowTitle:str)-> tuple:
        TargetWindowHandle = ctypes.windll.user32.FindWindowW(0, TargetWindowTitle)
        Rectangle = ctypes.wintypes.RECT()
        ctypes.windll.user32.GetWindowRect(TargetWindowHandle, ctypes.pointer(Rectangle))
        return (Rectangle.left, Rectangle.top, Rectangle.right, Rectangle.bottom)

    # ウィンドウ一覧を更新
    def update_command_window_name(self):
        self.window_name_list = self.window_title_delete_null(self.get_window_title())
        for i, window_name in enumerate(self.window_name_list):
            self.popUpMenu_window.entryconfigure(i, label=window_name, command= lambda window_name = window_name: self.command_window_change(window_name))



if __name__ == '__main__':
    root = tk.Tk()
    gui = viewerGUI(master=root)
