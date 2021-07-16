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

        self.is_focus_window = False
        self.color_filter = "default"
        self.is_image_flip_horizontal = False
        self.is_image_flip_upside_down =False
        self.focus_window_name = ""
        self.window_name_list = self.window_title_delete_null(self.get_window_title())
        self.scale = 2

        self.create_canvas()
        self.create_popupmenu()
        self.create_key_handler()
        self.create_mouse_handler()
        
        self.update()
        self.mainloop()

    # ----------------------画像表示canvas設定----------------------
    def create_canvas(self):
        self.fm_upper = tk.Frame(self.master)
        self.fm_upper.pack(fill=tk.BOTH, expand=1)
        # canvas作成
        self.canvas = tk.Canvas(self.fm_upper, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=tk.BOTH, expand=1)

    # 画像を更新する処理
    def update_canvas(self):

        if self.focus_window_name == "":
            self.is_focus_window = False
            return
        # ハンドルからキャプチャウィンドウのサイズを取得
        self.window_size = self.GetWindowRectFromHandle(self.window_handle)
        # 画像読み込み(mssとImageGrabどっちがいいのかまだわかってない)
        self.grab_image = mss.mss().grab(self.window_size)
        # self.grab_image = ImageGrab.grab(self.window_size)

        # 画像が読み込めなかった場合（ウィンドウが閉じたなど）
        if self.grab_image.width == 0 and self.grab_image.height == 0 :
            self.is_focus_window = False
            self.canvas.delete("all")
            # 閉じられる前と同じ名前のウィンドウが開いたら自動的にハンドル取得
            self.window_handle = viewerGUI.GetWindowHandleFromName(self.focus_window_name)
            return

        self.is_focus_window = True

        # 配列に変換
        self.cv_img = np.array(self.grab_image)

        # canvasの大きさ取得
        self.canvas_top = self.canvas.winfo_x()
        self.canvas_bottom = self.canvas.winfo_x() + self.canvas.winfo_width()
        self.canvas_left = self.canvas.winfo_y()
        self.canvas_right = self.canvas.winfo_y() + self.canvas.winfo_height()

        # 倍率反映
        self.cv_img = cv2.resize(self.cv_img, dsize=None, fx=self.scale, fy=self.scale)

        # canvasからはみ出た部分は削除
        self.cv_img =self.cv_img[self.canvas_left:self.canvas_right,self.canvas_top:self.canvas_bottom ]

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

    # ----------------------マウス入力設定----------------------
    def create_mouse_handler(self):
        # root.bind("<Motion>", self.mouse_move)
    
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<MouseWheel>", self.wheel)
        self.canvas.pack()

    # マウスダウン
    def click(self, event):
        if not self.is_focus_window: return
        self.canvas.scan_mark(event.x, event.y)

    # マウスムーブ
    def drag(self, event):
        if not self.is_focus_window: return
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    # マウスホイール
    def wheel(self, event):
        if not self.is_focus_window: return
        if event.delta > 0: # 向きの検出
            if self.scale > 3: return
            self.scale_at(1.25, event.x, event.y) # 拡大
        else:
            if self.scale < 0.5: return
            self.scale_at(0.8, event.x, event.y) # 縮小

    # ----------------------画像表示変換の設定----------------------
    # 拡大縮小
    def scale_at(self, scale:float, cx:float, cy:float):
        self.scale *= scale
        # 座標(cx, cy)を中心に拡大縮小

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
        self.window_handle = viewerGUI.GetWindowHandleFromName(self.focus_window_name)

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
    def GetWindowHandleFromName(TargetWindowTitle:str)-> tuple:
        TargetWindowHandle = ctypes.windll.user32.FindWindowW(0, TargetWindowTitle) # ウィンドウハンドル取得
        return TargetWindowHandle
        

    # ウィンドウハンドルから位置を取得
    def GetWindowRectFromHandle(self, TargetWindowHandle):
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
