# coding: utf-8


import tkinter as tk
import tkinter.ttk as ttk
import imgFrame


WIDTH = 500
HEIGHT = 500


class PanedWindow(tk.Frame):
    def __init__(self, root, master=None):
        super().__init__(master)

        self.p_window_count = 1  # アクティブ中のウィンドウの数
        imgFrame.frameGUI.p_window_count = self.p_window_count

        # 親PanedWindowの作成
        self.parent_p_window = ttk.PanedWindow(root, orient='horizontal')
        self.parent_p_window.pack(expand=True, fill=tk.BOTH)

        # PanedWindowの作成
        p_window = ttk.PanedWindow(root, orient='horizontal')
        # p_window.pack(expand = True, fill = tk.BOTH)
        self.parent_p_window.add(p_window)

        # Frameの作成
        frame = imgFrame.frameGUI(root, WIDTH, HEIGHT)

        frame.menu.add_command(label='ウィンドウを縦に分割',
                               underline=5,
                               command=lambda:
                               self.create_p_window(p_window,
                                                    frame, "|", root))
        frame.menu.add_command(label='ウィンドウを横に分割',
                               underline=5,
                               command=lambda:
                               self.create_p_window(p_window,
                                                    frame, "-", root))
        frame.menu.add_command(label='ウィンドウを削除',
                               underline=5,
                               command=lambda:
                               self.forget_frame(self.parent_p_window,
                                                 frame, frame, root))
        frame.update()

        # フレームをPanedWindowに追加
        p_window.add(frame.app_frame)

    def create_p_window(self, parent_p_window,
                        parent_frame, direction, root):

        # PanedWindowの作成
        if direction == "|":  # 垂直方向のpanedWindowを作成
            p_window = ttk.PanedWindow(parent_p_window,
                                       orient='horizontal')
            parent_frame.resize_half_frame_y()  # 親Frameの横サイズを半分にする
        elif direction == "-":  # 平行方向のpanedWindowを作成
            p_window = ttk.PanedWindow(parent_p_window,
                                       orient='vertical')
            parent_frame.resize_half_frame_x()  # 親Frameの縦サイズを半分にする

        # 親PanedWindowに新しいPanedWindowを追加
        if len(parent_p_window.panes()) == 1:  # 初回は窓が一つしかないため
            parent_p_window.add(p_window)

        elif len(parent_p_window.panes()) == 2:  # ２分割目以降
            parent_p_window_0 = parent_p_window.nametowidget(
                parent_p_window.panes()[0])
            parent_p_window_1 = parent_p_window.nametowidget(
                parent_p_window.panes()[1])

            # １番目のFrameの分割を選択していた
            if parent_p_window_0 == parent_frame.app_frame:
                parent_p_window.insert(0, p_window)

            # ２番目のFrameの分割を選択していた
            elif parent_p_window_1 == parent_frame.app_frame:
                parent_p_window.add(p_window)

        # 親FrameのparentPanedWindowとparentFrameWidgetを更新
        parent_frame.menu.entryconfigure('ウィンドウを縦に分割',
                                         command=lambda:
                                         self.create_p_window(p_window,
                                                              parent_frame,
                                                              "|", root))

        parent_frame.menu.entryconfigure('ウィンドウを横に分割',
                                         command=lambda:
                                         self.create_p_window(p_window,
                                                              parent_frame,
                                                              "-", root))

        parent_frame.menu.entryconfigure('ウィンドウを削除',
                                         command=lambda:
                                         self.forget_frame(parent_p_window,
                                                           p_window,
                                                           parent_frame,
                                                           root))

        # 新しいFrameを作成
        frame = imgFrame.frameGUI(root,
                                  parent_frame.winfo_width(),
                                  parent_frame.winfo_height())

        # 新しいFrameの機能を追加
        frame.menu.add_command(label='ウィンドウを縦に分割',
                               underline=5,
                               command=lambda:
                               self.create_p_window(p_window,
                                                    frame, "|", root))
        frame.menu.add_command(label='ウィンドウを横に分割',
                               underline=5,
                               command=lambda:
                               self.create_p_window(p_window,
                                                    frame, "-", root))
        frame.menu.add_command(label='ウィンドウを削除',
                               underline=5,
                               command=lambda:
                               self.forget_frame(parent_p_window,
                                                 p_window, frame, root)
                               )
        frame.update()

        # FrameをPanedWindowに追加
        p_window.add(parent_frame.app_frame)  # 親Frame
        p_window.add(frame.app_frame)  # 新しいFrame

        self.p_window_count += 1
        imgFrame.frameGUI.p_window_count = self.p_window_count

    # ウィンドウの削除
    def forget_frame(self, parent_parent_p_window,
                     parent_p_window, parent_frame, root):
        parent_p_window.forget(parent_frame.app_frame)
        # panedWindowの中のFrameが全部削除されたらpanedWindowも削除する
        if len(parent_p_window.panes()) == 0:
            parent_parent_p_window.forget(parent_p_window)

        self.p_window_count -= 1
        imgFrame.frameGUI.p_window_count = self.p_window_count
