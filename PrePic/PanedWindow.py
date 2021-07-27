# coding: utf-8


import tkinter as tk
import tkinter.ttk as ttk
import imgFrame


WIDTH = 500
HEIGHT = 500


class PanedWindow(tk.Frame):
    def __init__(self, root, master=None):
        super().__init__(master)

        self.panedWindow_count = 1  # アクティブ中のウィンドウの数
        imgFrame.frameGUI.panedWindow_count = self.panedWindow_count

        # 親PanedWindowの作成
        self.parentWindow = ttk.PanedWindow(root, orient='horizontal')
        self.parentWindow.pack(expand=True, fill=tk.BOTH)

        # PanedWindowの作成
        panedWindow = ttk.PanedWindow(root, orient='horizontal')
        # panedWindow.pack(expand = True, fill = tk.BOTH)
        self.parentWindow.add(panedWindow)

        # Frameの作成
        frameWidget = imgFrame.frameGUI(root, WIDTH, HEIGHT)

        frameWidget.popUpMenu.add_command(label='ウィンドウを縦に分割',
                                          underline=5,
                                          command=lambda:
                                          self.create_paned_frame(panedWindow,
                                                                  frameWidget,
                                                                  "|", root))
        frameWidget.popUpMenu.add_command(label='ウィンドウを横に分割',
                                          underline=5,
                                          command=lambda:
                                          self.create_paned_frame(panedWindow,
                                                                  frameWidget,
                                                                  "-", root))
        frameWidget.popUpMenu.add_command(label='ウィンドウを削除',
                                          underline=5,
                                          command=lambda:
                                          self.forget_paned_frame(self.parentWindow,
                                                                  frameWidget,
                                                                  frameWidget,
                                                                  root))
        frameWidget.update()

        # フレームをPanedWindowに追加
        panedWindow.add(frameWidget.app_frame)

    def create_paned_frame(self, parentPanedWindow,
                           parentFrameWidget, direction, root):

        # PanedWindowの作成
        if direction == "|":  # 垂直方向のpanedWindowを作成
            panedWindow = ttk.PanedWindow(parentPanedWindow,
                                          orient='horizontal')
            parentFrameWidget.resize_frame_y()  # 親Frameの横サイズを半分にする
        elif direction == "-":  # 平行方向のpanedWindowを作成
            panedWindow = ttk.PanedWindow(parentPanedWindow,
                                          orient='vertical')
            parentFrameWidget.resize_frame_x()  # 親Frameの縦サイズを半分にする

        # 親PanedWindowに新しいPanedWindowを追加
        parentPanedWindowWidget_0 = parentPanedWindow.nametowidget(
            parentPanedWindow.panes()[0])
        if len(parentPanedWindow.panes()) == 1:  # 初回は窓が一つしかないため
            parentPanedWindow.add(panedWindow)
        elif len(parentPanedWindow.panes()) == 2:  # ２分割目以降
            parentPanedWindowWidget_1 = parentPanedWindow.nametowidget(
                parentPanedWindow.panes()[1])
            # １番目のFrameの分割を選択していた
            if parentPanedWindowWidget_0 == parentFrameWidget.app_frame:
                parentPanedWindow.insert(0, panedWindow)
            # ２番目のFrameの分割を選択していた
            elif parentPanedWindowWidget_1 == parentFrameWidget.app_frame:
                parentPanedWindow.add(panedWindow)

        # 親FrameのparentPanedWindowとparentFrameWidgetを更新
        parentFrameWidget.popUpMenu.entryconfigure('ウィンドウを縦に分割',
                                                   command=lambda:
                                                   self.create_paned_frame(panedWindow,
                                                                           parentFrameWidget,
                                                                           "|", root))

        parentFrameWidget.popUpMenu.entryconfigure('ウィンドウを横に分割',
                                                   command=lambda:
                                                   self.create_paned_frame(panedWindow,
                                                                           parentFrameWidget,
                                                                           "-", root))

        parentFrameWidget.popUpMenu.entryconfigure('ウィンドウを削除',
                                                   command=lambda:
                                                   self.forget_paned_frame(parentPanedWindow, panedWindow,
                                                                           parentFrameWidget, root))

        # 新しいFrameを作成
        frameWidget = imgFrame.frameGUI(root, parentFrameWidget.winfo_width(),
                                        parentFrameWidget.winfo_height())

        # 新しいFrameの機能を追加
        frameWidget.popUpMenu.add_command(label='ウィンドウを縦に分割',
                                          underline=5,
                                          command=lambda:
                                          self.create_paned_frame(
                                              panedWindow, frameWidget,
                                              "|", root))
        frameWidget.popUpMenu.add_command(label='ウィンドウを横に分割',
                                          underline=5,
                                          command=lambda:
                                          self.create_paned_frame(panedWindow, frameWidget,
                                                                  "-", root))
        frameWidget.popUpMenu.add_command(label='ウィンドウを削除', underline=5,
                                          command=lambda:
                                          self.forget_paned_frame(parentPanedWindow, panedWindow,
                                                                  frameWidget, root),
                                          state='normal')
        frameWidget.update()

        # FrameをPanedWindowに追加
        panedWindow.add(parentFrameWidget.app_frame)  # 親Frame
        panedWindow.add(frameWidget.app_frame)  # 新しいFrame

        self.panedWindow_count += 1
        imgFrame.frameGUI.panedWindow_count = self.panedWindow_count

    # ウィンドウの削除
    def forget_paned_frame(self, parentParentPanedWindow,
                           parentPanedWindow, parentFrameWidget, root):
        parentPanedWindow.forget(parentFrameWidget.app_frame)
        # panedWindowの中のFrameが全部削除されたらpanedWindowも削除する
        if len(parentPanedWindow.panes()) == 0:
            parentParentPanedWindow.forget(parentPanedWindow)

        self.panedWindow_count -= 1
        imgFrame.frameGUI.panedWindow_count = self.panedWindow_count
