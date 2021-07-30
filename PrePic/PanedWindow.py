# coding: utf-8


import tkinter as tk
import tkinter.ttk as ttk
import imgFrame


WIDTH = 500
HEIGHT = 500


class PanedWindow(tk.Frame):
    def __init__(self, root, master=None):
        super().__init__(master)

        self.paned_window_count = 1  # アクティブ中のウィンドウの数
        imgFrame.frameGUI.paned_window_count = self.paned_window_count

        # 親PanedWindowの作成
        self.parent_window = ttk.PanedWindow(root, orient='horizontal')
        self.parent_window.pack(expand=True, fill=tk.BOTH)

        # PanedWindowの作成
        paned_window = ttk.PanedWindow(root, orient='horizontal')
        # paned_window.pack(expand = True, fill = tk.BOTH)
        self.parent_window.add(paned_window)

        # Frameの作成
        frame_widget = imgFrame.frameGUI(root, WIDTH, HEIGHT)

        frame_widget.popup_menu.add_command(label='ウィンドウを縦に分割',
                                            underline=5,
                                            command=lambda:
                                            self.create_paned_frame(paned_window,
                                                                    frame_widget,
                                                                    "|", root))
        frame_widget.popup_menu.add_command(label='ウィンドウを横に分割',
                                            underline=5,
                                            command=lambda:
                                            self.create_paned_frame(paned_window,
                                                                    frame_widget,
                                                                    "-", root))
        frame_widget.popup_menu.add_command(label='ウィンドウを削除',
                                            underline=5,
                                            command=lambda:
                                            self.forget_paned_frame(self.parent_window,
                                                                    frame_widget,
                                                                    frame_widget,
                                                                    root))
        frame_widget.update()

        # フレームをPanedWindowに追加
        paned_window.add(frame_widget.app_frame)

    def create_paned_frame(self, parent_paned_window,
                           parent_frame_widget, direction, root):

        # PanedWindowの作成
        if direction == "|":  # 垂直方向のpanedWindowを作成
            paned_window = ttk.PanedWindow(parent_paned_window,
                                           orient='horizontal')
            parent_frame_widget.resize_frame_y()  # 親Frameの横サイズを半分にする
        elif direction == "-":  # 平行方向のpanedWindowを作成
            paned_window = ttk.PanedWindow(parent_paned_window,
                                           orient='vertical')
            parent_frame_widget.resize_frame_x()  # 親Frameの縦サイズを半分にする

        # 親PanedWindowに新しいPanedWindowを追加
        parent_paned_window_widget_0 = parent_paned_window.nametowidget(
            parent_paned_window.panes()[0])
        if len(parent_paned_window.panes()) == 1:  # 初回は窓が一つしかないため
            parent_paned_window.add(paned_window)
        elif len(parent_paned_window.panes()) == 2:  # ２分割目以降
            parent_paned_window_widget_1 = parent_paned_window.nametowidget(
                parent_paned_window.panes()[1])
            # １番目のFrameの分割を選択していた
            if parent_paned_window_widget_0 == parent_frame_widget.app_frame:
                parent_paned_window.insert(0, paned_window)
            # ２番目のFrameの分割を選択していた
            elif parent_paned_window_widget_1 == parent_frame_widget.app_frame:
                parent_paned_window.add(paned_window)

        # 親FrameのparentPanedWindowとparentFrameWidgetを更新
        parent_frame_widget.popup_menu.entryconfigure('ウィンドウを縦に分割',
                                                      command=lambda:
                                                      self.create_paned_frame(paned_window,
                                                                              parent_frame_widget,
                                                                              "|", root))

        parent_frame_widget.popup_menu.entryconfigure('ウィンドウを横に分割',
                                                      command=lambda:
                                                      self.create_paned_frame(paned_window,
                                                                              parent_frame_widget,
                                                                              "-", root))

        parent_frame_widget.popup_menu.entryconfigure('ウィンドウを削除',
                                                      command=lambda:
                                                      self.forget_paned_frame(parent_paned_window, paned_window,
                                                                              parent_frame_widget, root))

        # 新しいFrameを作成
        frame_widget = imgFrame.frameGUI(root, parent_frame_widget.winfo_width(),
                                         parent_frame_widget.winfo_height())

        # 新しいFrameの機能を追加
        frame_widget.popup_menu.add_command(label='ウィンドウを縦に分割',
                                            underline=5,
                                            command=lambda:
                                            self.create_paned_frame(
                                                paned_window, frame_widget,
                                                "|", root))
        frame_widget.popup_menu.add_command(label='ウィンドウを横に分割',
                                            underline=5,
                                            command=lambda:
                                            self.create_paned_frame(paned_window, frame_widget,
                                                                    "-", root))
        frame_widget.popup_menu.add_command(label='ウィンドウを削除', underline=5,
                                            command=lambda:
                                            self.forget_paned_frame(parent_paned_window, paned_window,
                                                                    frame_widget, root),
                                            state='normal')
        frame_widget.update()

        # FrameをPanedWindowに追加
        paned_window.add(parent_frame_widget.app_frame)  # 親Frame
        paned_window.add(frame_widget.app_frame)  # 新しいFrame

        self.paned_window_count += 1
        imgFrame.frameGUI.paned_window_count = self.paned_window_count

    # ウィンドウの削除
    def forget_paned_frame(self, parent_parent_paned_window,
                           parent_paned_window, parent_frame_widget, root):
        parent_paned_window.forget(parent_frame_widget.app_frame)
        # panedWindowの中のFrameが全部削除されたらpanedWindowも削除する
        if len(parent_paned_window.panes()) == 0:
            parent_parent_paned_window.forget(parent_paned_window)

        self.paned_window_count -= 1
        imgFrame.frameGUI.paned_window_count = self.paned_window_count
