# coding: utf-8

import tkinter as tk
import tkinter.ttk as ttk
import PanedWindow


class viewerGUI(ttk.Frame):
    def __init__(self, root, master=None):
        super().__init__(master)

        # PanedWindowの作成
        self.paned_window = PanedWindow.PanedWindow(root)

        self.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    gui = viewerGUI(root, master=root)
