# coding: utf-8

import cv2
import numpy as np
from PIL import ImageGrab
from PIL import Image, ImageTk
import ctypes
import ctypes.wintypes

import tkinter as tk
import tkinter.ttk as ttk
import mss
import sys

SCALEMAX = 1
SCALEMIN = 0.5


class frameGUI(tk.Frame):
    p_window_count = 1                  # ウィンドウの数（削除する有効化無効化判定に使用）

    def __init__(self, root, frame_width, frame_height, master=None):
        super().__init__(master)
        self.root = root
        self.frame_width = frame_width  # frame生成時の横の大きさ（親パネルの2分の1）
        self.frame_height = frame_height  # frame生成時の縦の大きさ（親パネルの2分の1）

        self.is_focus_window = False                # focusしているウィンドウがあるか
        self.color_filter = "default"               # 色変化
        self.is_image_flip_horizontal = False       # 左右反転有効有無
        self.is_image_flip_upside_down = False       # 上下反転有効有無
        self.focus_window_title = ""                 # focusしているウィンドウの名前
        self.window_title_list = self.get_window_title_list()  # 右クリック選択用
        self.scale = 1                              # 初期拡大率
        self.isOnMouse = False                      # frameにマウスオーバーしているか

        root.protocol('WM_DELETE_WINDOW', self.do_something)
        self.create_frame()
        self.create_canvas()
        self.move_img()
        self.create_popupmenu()
        self.create_key_handler()
        self.create_mouse_handler()

    # ----------------------frame設定----------------------
    def create_frame(self):
        self.app_frame = tk.Frame(self.root)
        self.app_frame.bind("<Enter>", self.enter_mouse)
        self.app_frame.bind("<Leave>", self.leave_mouse)
        # Frameの大きさに合わせてcanvasの中身を調整
        self.app_frame.bind('<Configure>', self.configure_frame_move_img)
        self.app_frame.pack(expand=False)

    def resize_half_frame_y(self):
        self.app_frame.configure(width=self.app_frame.winfo_width()/2)

    def resize_half_frame_x(self):
        self.app_frame.configure(height=self.app_frame.winfo_height()/2)

    def enter_mouse(self, event):
        self.canvas.configure(background='#CCFFFF')
        self.isOnMouse = True

    def leave_mouse(self, event):
        self.canvas.configure(background='SystemButtonFace')
        self.isOnMouse = False

    # ----------------------画像表示canvas設定----------------------
    def create_canvas(self):
        # スクロールバー作成
        self.create_scrollbar()

        # canvas作成
        self.canvas = tk.Canvas(self.app_frame, bd=0,
                                highlightthickness=0,
                                yscrollcommand=self.vscrollbar.set,
                                xscrollcommand=self.hscrollbar.set,
                                width=self.frame_width,
                                height=self.frame_height, relief="ridge",
                                borderwidth="2")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # self.canvas.pack(fill=tk.BOTH, expand=True)

        # スクロールバーをCanvasに関連付け
        self.vscrollbar.config(command=self.canvas.yview)
        self.hscrollbar.config(command=self.canvas.xview)

    def update(self):
        self.update_canvas()
        self.after(120, self.update)

    # 画像を更新する処理
    def update_canvas(self):
        # 画像処理系のコマンドをウィンドウ取得状態になったら有効化、ウィンドウ取得状態じゃなくなったら無効化
        menu_state = self.menu.entrycget('フィルタ', 'state')
        is_focus_window_state = (True
                                 if menu_state == 'normal'
                                 or menu_state == 'active'
                                 else False)
        if self.is_focus_window != is_focus_window_state:
            self.menu.entryconfigure('フィルタ',
                                     state=self.get_can_state())
            self.menu.entryconfigure('反転',
                                     state=self.get_can_state())

        if self.focus_window_title == "":
            self.is_focus_window = False
            return

        # ハンドルからキャプチャウィンドウのサイズを取得
        self.window_size = self.get_window_rect_from_handle(self.window_handle)
        # 画像読み込み(mssとImageGrabどっちがいいのかまだわかってない)
        self.grab_image = mss.mss().grab(self.window_size)
        # self.grab_image = ImageGrab.grab(self.window_size)

        # 画像が読み込めなかった場合（ウィンドウが閉じたなど）
        if self.grab_image.width == 0 and self.grab_image.height == 0:
            self.is_focus_window = False
            self.canvas.delete("all")
            # 閉じられる前と同じ名前のウィンドウが開いたら自動的にハンドル取得
            self.window_handle = frameGUI.get_window_handle_from_name(
                self.focus_window_title)
            return

        self.is_focus_window = True

        # 配列に変換
        self.cv_img = np.array(self.grab_image)

        # TODO: 拡大すると画像がはみ出て途中で切れるので、なんとかする
        # appの大きさ取得
        # self.app_top = self.app_frame.winfo_x()
        # self.app_bottom = self.app_frame.winfo_x() + self.app_frame.winfo_width()
        # self.app_left = self.app_frame.winfo_y()
        # self.app_right = self.app_frame.winfo_y() + self.app_frame.winfo_height()

        self.app_top = self.app_frame.winfo_rootx()
        self.app_bottom = (self.app_frame.winfo_rootx()
                           + self.app_frame.winfo_width())
        self.app_left = self.app_frame.winfo_rooty()
        self.app_right = (self.app_frame.winfo_rooty()
                          + self.app_frame.winfo_height())

        # canvasの大きさ取得
        self.canvas_top = self.canvas.winfo_x()
        self.canvas_bottom = self.canvas.winfo_x() + self.canvas.winfo_width()
        self.canvas_left = self.canvas.winfo_y()
        self.canvas_right = self.canvas.winfo_y() + self.canvas.winfo_height()

        # self.canvas_top = self.canvas.winfo_rootx()
        # self.canvas_bottom = self.canvas.winfo_rootx() + self.canvas.winfo_width()
        # self.canvas_left = self.canvas.winfo_rooty()
        # self.canvas_right = self.canvas.winfo_rooty() + self.canvas.winfo_height()

        # print('[',self.app_left,':',self.app_right,',',self.app_top,':',self.app_bottom ,']','[',self.canvas_left,':',self.canvas_right,',',self.canvas_top,':',self.canvas_bottom ,']')
        # print('[',self.app_left,':',self.app_right,',',self.app_top,':',self.app_bottom ,']','[',self.canvas_left,':',self.canvas_right,',',self.canvas_top,':',self.canvas_bottom ,']')

        # ウィンドウに合わせて画像の大きさを変化
        img_height = self.cv_img.shape[0]
        img_width = self.cv_img.shape[1]
        resize_scale_height = self.canvas_right / img_height
        resize_scale_width = self.canvas_bottom / img_width
        if resize_scale_height < 1 or resize_scale_width < 1:
            self.resize_scale = (resize_scale_height
                                 if resize_scale_height < resize_scale_width
                                 else resize_scale_width)

        # 最終的な倍率を計算
        self.scale = self.resize_scale * self.scroll_scale

        # 倍率を画像に反映
        self.cv_img = cv2.resize(self.cv_img, dsize=None,
                                 fx=self.scale, fy=self.scale)

        # print(self.app_frame.winfo_width())
        # # canvasからはみ出た部分は削除(廃止)
        # self.cv_img = self.cv_img[self.canvas_left:self.canvas_right,
        #                           self.canvas_top:self.canvas_bottom]

        # if self.app_left <
        # self.cv_img = self.cv_img[ self.app_left : self.app_right ,self.app_top : self.app_bottom ]

        # self.canvas.configure(width = self.cv_img.shape[1])
        # self.canvas.configure(height = self.cv_img.shape[0])

        # self.cv_img = self.cv_img[ self.app_left : self.app_right ,self.app_top : self.app_bottom ]

        # # 拡大率に合わせてスクロール範囲とスクロールバーの長さの変更(廃止)
        # self.scrollregion_x = self.canvas_right * 2 * self.scroll_scale
        # self.scrollregion_y = self.canvas_bottom * 2 * self.scroll_scale

        self.scrollregion_x = self.canvas_right * 2
        self.scrollregion_y = self.canvas_bottom * 2
        # スクロール範囲
        self.canvas.configure(scrollregion=(-self.scrollregion_y,
                                            -self.scrollregion_x,
                                            self.scrollregion_y,
                                            self.scrollregion_x))

        # 色変換
        if self.color_filter == "default":
            self.cv_img = cv2.cvtColor(self.cv_img, cv2.COLOR_RGB2BGR)
        elif self.color_filter == "gray":
            self.cv_img = cv2.cvtColor(self.cv_img, cv2.COLOR_BGR2GRAY)
        elif self.color_filter == "inversion":
            self.cv_img = cv2.cvtColor(self.cv_img, cv2.COLOR_RGB2BGR)
            self.cv_img = cv2.bitwise_not(self.cv_img)
        # 画像編集
        if self.is_image_flip_horizontal:
            self.cv_img = cv2.flip(self.cv_img, 1)
        if self.is_image_flip_upside_down:
            self.cv_img = cv2.flip(self.cv_img, 0)

        # canvasに画像を表示
        self.im = ImageTk.PhotoImage(image=Image.fromarray(self.cv_img))
        # 開きたては真ん中に表示　それ以外はウィンドウの大きさによって位置を変化
        self.canvas.create_image(self.image_move_wonfo_x,
                                 self.image_move_wonfo_y,
                                 image=self.im)

    # canvasの中身の位置を変更
    def configure_frame_move_img(self, event):
        self.move_img()

    def move_img(self):
        self.canvas_w = self.canvas.winfo_width()
        self.canvas_h = self.canvas.winfo_height()
        self.image_move_wonfo_x = self.canvas_w / 2
        self.image_move_wonfo_y = self.canvas_h / 2

    # canvas初期化
    def clean_canvas(self):
        self.move_img()
        self.color_filter = "default"
        self.is_image_flip_horizontal = False
        self.is_image_flip_upside_down = False
        self.scroll_scale = 1

    # ----------------------キー入力設定----------------------
    def key_handler(self, event):
        print(event.keycode)

    def create_key_handler(self):
        self.root.bind("<KeyPress>", self.key_handler)

    # ----------------------マウス入力設定----------------------
    def create_mouse_handler(self):
        # self.root.bind("<Motion>", self.mouse_move)

        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<MouseWheel>", self.wheel)
        self.canvas.pack()

    # マウスダウン
    def click(self, event):
        if not self.is_focus_window:
            return
        self.canvas.scan_mark(event.x, event.y)

    # マウスムーブ
    def drag(self, event):
        if not self.is_focus_window:
            return
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    # マウスホイール
    def wheel(self, event):
        if not self.is_focus_window:
            return
        if event.delta > 0:  # 向きの検出
            if self.scroll_scale > SCALEMAX:
                return
            self.scroll_scale_at(1.25, event.x, event.y)  # 拡大
        else:
            if self.scroll_scale < SCALEMIN:
                return
            self.scroll_scale_at(0.8, event.x, event.y)  # 縮小

    # ----------------------画像表示変換の設定----------------------
    # 拡大縮小
    def scroll_scale_at(self, scale: float, cx: float, cy: float):
        self.scroll_scale *= scale
        # self.canvas.configure(width = self.canvas_bottom * scale)
        # self.canvas.configure(height = self.canvas_right * scale)

        # 座標(cx, cy)を中心に拡大縮小

    # ----------------------スクロールバー作成----------------------
    def create_scrollbar(self):
        # 縦スクロールバー
        self.vscrollbar = ttk.Scrollbar(self.app_frame, orient=tk.VERTICAL)
        self.vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=False)

        # 横スクロールバー
        self.hscrollbar = ttk.Scrollbar(self.app_frame, orient=tk.HORIZONTAL)
        self.hscrollbar.pack(fill=tk.X, side=tk.BOTTOM, expand=False)

    # ----------------------ポップアップメニューの設定----------------------
    def show_popupmenu(self, event):
        # ウィンドウ一覧を更新
        self.update_window_title()

        # ウィンドウ削除の有効化、無効化
        self.menu.entryconfigure(
            'ウィンドウを削除', state=self.get_can_foget_state())

        # 何があっても終了を一番下に設置する
        # end = int(self.menu.index("end"))
        # for index in range(end):
        #     if self.menu.type(index) == "separator":
        #         self.menu.delete(index)
        #         break
        # self.menu.delete(7)
        # self.menu.add_separator()
        self.menu.delete("終了")
        self.menu.add_command(label="終了", command=self.finish)

        self.menu.post(event.x_root, event.y_root)

    def create_popupmenu(self):
        # ポップアップメニューの設定
        self.menu = tk.Menu(self.app_frame, tearoff=False)
        self.menu_filter = tk.Menu(self.menu, tearoff=False)
        self.menu_flip = tk.Menu(self.menu, tearoff=False)
        self.menu_window = tk.Menu(self.menu, tearoff=False)

        # [ポップアップメニュー] - [Command] - [フィルタ]
        self.menu.add_cascade(
            label='フィルタ', menu=self.menu_filter,
            under=5, state='disable')
        self.menu_filter.add_radiobutton(
            label='なし', underline=5,
            command=self.filter_default)
        self.menu_filter.add_radiobutton(
            label='グレースケール', underline=5,
            command=self.filter_gray)
        self.menu_filter.add_radiobutton(
            label='色反転', underline=5,
            command=self.filter_color_inversion)

        # [ポップアップメニュー] - [Command] - [反転]
        self.menu.add_cascade(
            label='反転', menu=self.menu_flip,
            under=5, state='disable')
        self.menu_flip.add_command(
            label='デフォルト', underline=5,
            command=self.flip_default)
        self.menu_flip.add_checkbutton(
            label='左右反転', underline=5,
            command=self.flip_horizontal)
        self.menu_flip.add_checkbutton(
            label='上下反転', underline=5,
            command=self.flip_upside_down)

        self.menu.add_separator()

        # [ポップアップメニュー] - [Command]
        self.menu.add_cascade(label='ウィンドウ切り替え',
                                    menu=self.menu_window)
        for window_title in self.window_title_list:
            self.menu_window.add_command(label=window_title,
                                         command=lambda
                                         window_title=window_title:
                                         self.window_change(window_title))

        self.menu.add_command(label="終了", command=self.finish)

        # 右クリックイベント関連付け
        self.canvas.bind("<Button-3>", self.show_popupmenu)

    # ----------------------ポップアップメニュー/画像処理の設定----------------------
    # フィルタ
    def filter_default(self):  # デフォルト
        self.color_filter = "default"

    def filter_gray(self):  # グレースケール
        if self.color_filter == "gray":
            self.color_filter = "default"
            self.menu_filter.invoke('なし')
        else:
            self.color_filter = "gray"

    def filter_color_inversion(self):  # 色反転
        if self.color_filter == "inversion":
            self.color_filter = "default"
            self.menu_filter.invoke('なし')
        else:
            self.color_filter = "inversion"

    # 反転
    def flip_default(self):  # デフォルト
        self.is_image_flip_horizontal = False
        self.is_image_flip_upside_down = False

    def flip_horizontal(self):  # 左右反転
        if not self.is_image_flip_horizontal:
            self.is_image_flip_horizontal = True
        else:
            self.is_image_flip_horizontal = False

    def flip_upside_down(self):  # 上下反転
        if not self.is_image_flip_upside_down:
            self.is_image_flip_upside_down = True
        else:
            self.is_image_flip_upside_down = False

    # focusしているウィンドウを変更
    def window_change(self, name):
        self.clean_canvas()
        self.focus_window_title = name
        self.window_handle = frameGUI.get_window_handle_from_name(
            self.focus_window_title)
        print(self.focus_window_title, 'を選択')

    # ウィンドウ削除の有効化無効化
    def get_can_foget_state(self):
        if frameGUI.p_window_count == 1:
            return 'disabled'
        else:
            return 'normal'

    # フィルタ・反転コマンドの有効化無効化
    def get_can_state(self):
        if self.is_focus_window is False:
            return 'disabled'
        else:
            return 'normal'

    # ----------------------終了時の処理----------------------
    def finish(self):
        print("終了")
        sys.exit()

    def do_something(self):
        print("終了")
        sys.exit()

    # ----------------------ウィンドウハンドラ----------------------
    # ウィンドウ一覧の名前を取得
    def get_window_title_list(self):
        return self.window_title_delete_null(
            self.get_window_title_list_include_null())

    def get_window_title_list_include_null(self):
        # このprintがないと何故か動かない
        print("")
        # コールバック関数を定義(定義のみで実行ではない) コールバック関数はctypes.WINFUNCTYPEで作成可能
        enum_windows_proc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(
            ctypes.c_int), ctypes.POINTER(ctypes.c_int))
        # 開いているウィンドウ一覧を取得
        EnumWindows = ctypes.windll.user32.EnumWindows
        # タイトル格納用変数
        title = []

        def foreach_window(hwnd, lparam):
            if ctypes.windll.user32.IsWindowVisible(hwnd):  # ウィンドウが表示されているかどうか
                # タイトルバー取得
                length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
                buff = ctypes.create_unicode_buffer(length + 1)
                ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
                title.append(buff.value)

                return True

        EnumWindows(enum_windows_proc(foreach_window), 0)

        return title

    # get_window_titleで取得したウィンドウ一覧には空の名前が含まれているため取り除く
    def window_title_delete_null(self, window_title_list):
        return [name for name in window_title_list if name != '']

    # ウィンドウの名前からウィンドウハンドルを取得
    def get_window_handle_from_name(window_title: str) -> tuple:
        window_handle = ctypes.windll.user32.FindWindowW(
            0, window_title)
        return window_handle

    # ウィンドウハンドルから位置を取得
    def get_window_rect_from_handle(self, window_handle):
        Rectangle = ctypes.wintypes.RECT()
        ctypes.windll.user32.GetWindowRect(
            window_handle, ctypes.pointer(Rectangle))
        # print(Rectangle.left,',', Rectangle.top,',', Rectangle.right,',' ,Rectangle.bottom)
        return (Rectangle.left,
                Rectangle.top,
                Rectangle.right,
                Rectangle.bottom)

    # ウィンドウ一覧を更新

    def update_window_title(self):
        self.window_title_list = self.get_window_title_list()
        for i, window_title in enumerate(self.window_title_list):
            self.menu_window.entryconfigure(i, label=window_title,
                                            command=lambda
                                            window_title=window_title:
                                            self.window_change(window_title))
