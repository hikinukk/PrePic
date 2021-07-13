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

if __name__ == '__main__':
    root = tk.Tk()
    gui = viewerGUI(master=root)
    gui.mainloop()
