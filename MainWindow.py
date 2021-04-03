import os
import sys
from datetime import datetime

import win32api
import win32con
import win32gui
import win32ui
from PIL import Image
from PyQt5 import QtWidgets, QtGui

from Rooms.Poker888 import Table_888 as tab_888


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        # Tables --------------------------------------------------------------
        # table_size = (682, 539)
        self.table_width = 682
        self.table_height = 539
        # table_01
        self.table_01 = tab_888.Table()
        self.table_01.set_areas(0, 94)
        # self.table_01.set_areas(0, 0)
        # table_02
        self.table_02 = tab_888.Table()
        self.table_02.set_areas(self.table_width, 0)
        # QWidget -------------------------------------------------------------
        QtWidgets.QWidget.__init__(self, parent)
        self.image = ''
        self.msTimer = 1500
        self.timer_id = 0
        self.setWindowTitle('Python')
        self.vbox_main = QtWidgets.QVBoxLayout()
        self.tabWidget = QtWidgets.QTabWidget()
        # tab1 ----------------------------------------------------------------
        self.tab1 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab1, 'Table 1')
        # добавим tab1_table
        self.tab1_vbox = QtWidgets.QVBoxLayout(self.tab1)
        self.tab1_vbox.setContentsMargins(0, 0, 0, 0)
        # добавление элементов в контейнер
        self.tab1_table = QtWidgets.QTableView(self.tab1)
        self.tab1_vbox.addWidget(self.tab1_table)
        # tab2 ----------------------------------------------------------------
        self.tab2 = QtWidgets.QWidget()
        self.tabWidget.addTab(self.tab2, 'Table 2')
        # добавим tab2_table
        self.tab2_vbox = QtWidgets.QVBoxLayout(self.tab2)
        self.tab2_vbox.setContentsMargins(0, 0, 0, 0)
        # добавление элементов в контейнер
        self.tab2_table = QtWidgets.QTableView(self.tab2)
        self.tab2_vbox.addWidget(self.tab2_table)
        # когда закончили с вкладками - добавляем tabWidget -------------------
        self.vbox_main.addWidget(self.tabWidget)
        self.tabWidget.setCurrentIndex(0)

        # создадим control_panel ----------------------------------------------
        self.control_panel = QtWidgets.QWidget()
        # заполним control_panel
        self.control_panel_hbox = QtWidgets.QHBoxLayout(self.control_panel)
        self.control_panel_hbox.setContentsMargins(0, 0, 0, 0)
        # добавим контейнер для QLabel основной -------------------------------
        self.control_panel_hbox_vbox = QtWidgets.QVBoxLayout(self.control_panel)
        self.control_panel_hbox_vbox.setContentsMargins(0, 0, 0, 0)
        self.control_panel_hbox.addLayout(self.control_panel_hbox_vbox)
        # добавим 2 контейнера для QLabel дополнительных ----------------------
        self.control_panel_hbox_vbox_hbox1 = QtWidgets.QHBoxLayout(self.control_panel)
        self.control_panel_hbox_vbox_hbox1.setContentsMargins(0, 0, 0, 0)
        self.control_panel_hbox_vbox.addLayout(self.control_panel_hbox_vbox_hbox1)
        self.control_panel_hbox_vbox_hbox2 = QtWidgets.QHBoxLayout(self.control_panel)
        self.control_panel_hbox_vbox_hbox2.setContentsMargins(0, 0, 0, 0)
        self.control_panel_hbox_vbox.addLayout(self.control_panel_hbox_vbox_hbox2)
        # добавление элементов в контейнер control_panel_hbox_vbox_hbox1 ------
        self.CheckBox1 = QtWidgets.QCheckBox(self.control_panel)
        self.CheckBox1.setChecked(True)
        self.control_panel_hbox_vbox_hbox1.addWidget(self.CheckBox1)
        self.label1 = QtWidgets.QLabel('1) -', self.control_panel)
        self.label1.setFont(QtGui.QFont('Consolas', 16))
        self.control_panel_hbox_vbox_hbox1.addWidget(self.label1, True)
        # добавление элементов в контейнер control_panel_hbox_vbox_hbox2 ------
        self.CheckBox2 = QtWidgets.QCheckBox(self.control_panel)
        self.CheckBox2.setChecked(False)
        self.control_panel_hbox_vbox_hbox2.addWidget(self.CheckBox2)
        self.label2 = QtWidgets.QLabel('2) -', self.control_panel)
        self.label2.setFont(QtGui.QFont('Consolas', 16))
        self.control_panel_hbox_vbox_hbox2.addWidget(self.label2, True)
        # добавление элементов в контейнер QPushButton ------------------------
        self.button1 = QtWidgets.QPushButton(self.control_panel)
        self.button1.setText('Start')
        self.control_panel_hbox.addWidget(self.button1)
        self.button2 = QtWidgets.QPushButton(self.control_panel)
        self.button2.setText('Stop')
        self.button2.setEnabled(False)
        self.control_panel_hbox.addWidget(self.button2)
        self.button3 = QtWidgets.QPushButton(self.control_panel)
        self.button3.setText('PrtScr')
        self.button3.setFixedWidth(50)
        self.control_panel_hbox.addWidget(self.button3)

        self.vbox_main.addWidget(self.control_panel)
        self.vbox_main.addLayout(self.control_panel_hbox)
        self.setLayout(self.vbox_main)

        self.filling()
        self.button1.clicked.connect(self.on_clicked_button1)
        self.button2.clicked.connect(self.on_clicked_button2)
        self.button3.clicked.connect(self.on_clicked_button3)

    def filling(self):
        """Заполнение таблиц значениями"""
        # таблица self.tab1_table & self.tab2_table
        self.sti_01 = QtGui.QStandardItemModel()
        self.sti_02 = QtGui.QStandardItemModel()
        self.list_h_headers = ['InTG', 'Stack', 'Bet', 'Posit.', 'Rank', 'Suit']
        self.list_v_headers = ['pl_1', 'pl_2', 'pl_3', 'pl_4', 'pl_5', 'pl_6',
                               'POT']
        self.tab1_table.setModel(self.sti_01)
        self.tab2_table.setModel(self.sti_02)
        self.ColWidth_RowHeight()

    def ColWidth_RowHeight(self):
        """Высота и ширина ячеек таблицы"""
        self.sti_01.setHorizontalHeaderLabels(self.list_h_headers)
        for col in range(0, len(self.list_h_headers)):
            self.tab1_table.setColumnWidth(col, 20)
        self.sti_01.setVerticalHeaderLabels(self.list_v_headers)
        for row in range(0, len(self.list_v_headers)):
            self.tab1_table.setRowHeight(row, 8)

        self.sti_02.setHorizontalHeaderLabels(self.list_h_headers)
        for col in range(0, len(self.list_h_headers)):
            self.tab2_table.setColumnWidth(col, 20)
        self.sti_02.setVerticalHeaderLabels(self.list_v_headers)
        for row in range(0, len(self.list_v_headers)):
            self.tab2_table.setRowHeight(row, 8)

    def timerEvent(self, *args, **kwargs):
        """Событие по таймеру"""
        self.on_clicked_button3()

    def take_screen(self):
        """scr1 + scr2"""
        if ('_scr' not in os.listdir()):
            os.mkdir('_scr')
        file_name = datetime.now().strftime('%Y%m%d_%H%M%S_%f')[:-3]

        # grab a handle to the main desktop window
        hdesktop = win32gui.GetDesktopWindow()
        # determine the size of all monitors in pixels
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
        # create a device context
        desktop_dc = win32gui.GetWindowDC(hdesktop)
        img_dc = win32ui.CreateDCFromHandle(desktop_dc)
        # create a memory based device context
        mem_dc = img_dc.CreateCompatibleDC()
        # create a bitmap object
        screenshot = win32ui.CreateBitmap()
        screenshot.CreateCompatibleBitmap(img_dc, width, height)
        mem_dc.SelectObject(screenshot)
        # copy the screen into our memory device context
        mem_dc.BitBlt((0, 0), (width, height), img_dc, (left, top), win32con.SRCCOPY)
        # save the BMP to a file
        screenshot.SaveBitmapFile(mem_dc, rf'_scr\{file_name}.bmp')
        # free our objects
        mem_dc.DeleteDC()
        win32gui.DeleteObject(screenshot.GetHandle())
        # convert BMP to PNG
        Image.open(rf'_scr\{file_name}.bmp').save(rf'_scr\{file_name}.png')
        os.remove(rf'_scr\{file_name}.bmp', dir_fd=None)
        # --------------------------------------------------------
        return file_name

    def on_clicked_button1(self):
        """Start"""
        self.timer_id = self.startTimer(self.msTimer)
        self.button1.setEnabled(False)
        self.button2.setEnabled(True)

    def on_clicked_button2(self):
        """Stop"""
        if self.timer_id:
            self.killTimer(self.timer_id)
            self.timer_id = 0
        self.button1.setEnabled(True)
        self.button2.setEnabled(False)

    def on_clicked_button3(self):
        """PrtScr"""
        file_name = self.take_screen()
        # file_name = '20210320_223030_083'
        try:
            self.image = Image.open(rf'_scr\{file_name}.png')
            self.gameplay()
        except:
            self.ColWidth_RowHeight()

    def gameplay(self):
        # table_01
        if self.CheckBox1.isChecked():
            # информация о кол-ве игроков
            self.table_01.pl_inTG(self.image, self.sti_01)
            # поймаем момент начала раздачи для определения позиции
            if self.table_01.pl_inTG_now > self.table_01.pl_inTG_last:
                # новая раздача
                self.table_01.new_deal = True
                self.table_01.stack(self.image, self.sti_01)
                self.table_01.bet_pot(self.image, self.sti_01)
                self.table_01.positions(self.sti_01)
            self.table_01.pl_inTG_last = self.table_01.pl_inTG_now
            # информация о моих картах
            self.table_01.my_cards(self.image, self.sti_01, self.label1, '1')
            if self.table_01.Im_inTG:
                # я в игре
                # информация о картах боарда
                self.table_01.board_cards(self.image, self.sti_01)
                self.table_01.if_my_turn(self.image)
                if self.table_01.my_turn:
                    # информация о стеках и ставках игроков
                    self.table_01.stack(self.image, self.sti_01)
                    self.table_01.bet_pot(self.image, self.sti_01)
                    # определим мой ход
                    my_move = self.table_01.my_move(self.sti_01, log_name='table_01')
                    self.label1.setText(f'1) {my_move}')
                    self.table_01.click_my_move(my_move, self.sti_01)
                else:
                    self.label1.setText('1) -')
        # table_02
        if self.CheckBox2.isChecked():
            # информация о кол-ве игроков
            self.table_02.pl_inTG(self.image, self.sti_02)
            # поймаем момент начала раздачи для определения позиции
            if self.table_02.pl_inTG_now > self.table_02.pl_inTG_last:
                # новая раздача
                self.table_02.new_deal = True
                self.table_02.stack(self.image, self.sti_02)
                self.table_02.bet_pot(self.image, self.sti_02)
                self.table_02.positions(self.sti_02)
            self.table_02.pl_inTG_last = self.table_02.pl_inTG_now
            # информация о моих картах
            self.table_02.my_cards(self.image, self.sti_02, self.label2, '2')
            if self.table_02.Im_inTG:
                # я в игре
                # информация о картах боарда
                self.table_02.board_cards(self.image, self.sti_02)
                self.table_02.if_my_turn(self.image)
                if self.table_02.my_turn:
                    # информация о стеках и ставках игроков
                    self.table_02.stack(self.image, self.sti_02)
                    self.table_02.bet_pot(self.image, self.sti_02)
                    # определим мой ход
                    my_move = self.table_02.my_move(self.sti_02, log_name='table_02')
                    self.label2.setText(f'2) {my_move}')
                    self.table_02.click_my_move(my_move, self.sti_02)
                else:
                    self.label2.setText('2) -')
        # установим размеры таблицы
        self.ColWidth_RowHeight()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = MainWindow()
    gui.resize(500, 300)
    gui.show()
    sys.exit(app.exec_())
