# coding: utf-8

from PIL import ImageGrab
from PIL import Image, ImageTk
import ctypes
import ctypes.wintypes

import tkinter as tk

WIDTH = 800
HEIGHT = 500
class viewerGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        self.create_canvas()
        self.create_popupmenu()

        self.mainloop()

    # ----------------------画像表示canvas設定----------------------
    def create_canvas(self):
        # canvas作成
        fm_upper = tk.Frame(self.master)
        fm_upper.pack(fill=tk.X, side=tk.TOP)
        self.canvas = tk.Canvas(fm_upper, width=WIDTH, height=HEIGHT)
        # 画像読み込み
        self.grab_image = ImageGrab.grab()
        # canvasに画像を表示
        self.im = ImageTk.PhotoImage(image=self.grab_image)
        self.canvas.create_image(0, 0, image=self.im, anchor='nw')
        self.canvas.pack()
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
            label = "Command1",
            command=self.command_1
        )
        # 右クリックイベント関連付け
        root.bind("<Button-3>", self.show_popupmenu)

    # Command1処理
    def command_1(self):
        print("Command_1")



if __name__ == '__main__':
    root = tk.Tk()
    gui = viewerGUI(master=root)
    gui.mainloop()
