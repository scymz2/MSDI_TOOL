# Mochuan Zhan , 2022/ 7/15 The University of Manchester
# UTF-8

# This is a program for selecting the ground control point
# If you need to resize your first image for feature matching, please input your new width and height, or
# just input the original size.

# if you use system other than Windows, please modify paths in function choose_file_1 and choose_file_2.

import sys
import cv2
import imghdr
import tkinter
from PIL import ImageGrab, ImageTk
import pyautogui as pag
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox, QDesktopWidget, QFileDialog, \
    QLabel, QHBoxLayout


def on_left_click_1(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        position = str(x) + ',' + str(y)
        # ex is the instance of the app
        ex.add_coord_1(position)
        scale = int(param.shape[1] / 600)
        cv2.circle(param, (x, y), 4 * scale, (0, 0, 225), scale)
        cv2.putText(param, xy, (x, y), cv2.FONT_HERSHEY_PLAIN, 2 * scale, (0, 0, 225), 2 * scale)
        cv2.imshow("img1", param)


def on_left_click_2(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        xy = "%d,%d" % (x, y)
        position = str(x) + ',' + str(y)
        # ex is the instance of the app
        ex.add_coord_2(position)
        scale = int(param.shape[1] / 600)
        cv2.circle(param, (x, y), 4 * scale, (0, 0, 225), scale)
        cv2.putText(param, xy, (x, y), cv2.FONT_HERSHEY_PLAIN, 2 * scale, (0, 0, 225), 2 * scale)
        cv2.imshow("img2", param)


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'gcp_selector'
        self.left = 10
        self.top = 10
        self.width = 650
        self.height = 900
        self.flag = False  # check whether root is created or not

        # cfg file content, please modify here if you want to
        self.text = '# SRC,im_name,name (im_num can be 1 or 2.)\nSRC1,EV_001.JPG\nSRC2,EV_002.JPG\n\n' \
                    '# GCP,im_num,x,y (im_num can be 1 or 2.  Order of im2 GCPs must be the same as those for im1.)'

        self.button1 = QPushButton('Create cfg', self)
        self.button2 = QPushButton('Select GCP', self)
        self.button3 = QPushButton('Choose image1', self)
        self.button4 = QPushButton('Choose image2', self)
        self.w = QtWidgets.QLineEdit()
        self.h = QtWidgets.QLineEdit()
        self.path1 = QtWidgets.QLineEdit()
        self.path2 = QtWidgets.QLineEdit()
        self.edit1 = QtWidgets.QTextEdit()
        self.edit2 = QtWidgets.QTextEdit()
        self.initUI()
        self.center()

    def create_tk(self):
        self.root = tkinter.Tk()
        self.root.geometry("200x120")
        self.root.wm_attributes('-topmost', 1)
        self.root.overrideredirect(True)
        self.canvas = tkinter.Canvas(self.root, width=200, height=120)
        self.canvas.pack(fill=tkinter.BOTH, expand=tkinter.YES)

    def center(self):
        # Put the window to the center of the screen
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def choose_file_1(self):
        m = QtWidgets.QFileDialog.getOpenFileName(None, 'Choose File', 'C:/')
        self.path1.setText(m[0])

    def choose_file_2(self):
        m = QtWidgets.QFileDialog.getOpenFileName(None, 'Choose File', 'C:/')
        self.path2.setText(m[0])

    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # One vertical layout
        layout = QVBoxLayout()
        # Two horizontal layout
        hlay = QHBoxLayout()
        hlayout = QHBoxLayout()
        hlayout2 = QHBoxLayout()

        # Form layout
        f1 = QtWidgets.QFormLayout()
        f2 = QtWidgets.QFormLayout()
        flayout1 = QtWidgets.QFormLayout()
        flayout2 = QtWidgets.QFormLayout()

        # line edit
        self.w.setPlaceholderText('0')
        self.h.setPlaceholderText('0')
        f1.addRow('Width:', self.w)
        f2.addRow('Height:', self.h)
        self.path1.setPlaceholderText('IMAGE PATH 1')
        self.path1.setReadOnly(True)
        self.path2.setPlaceholderText('IMAGE PATH 2')
        self.path2.setReadOnly(True)

        # put line and button together
        hlayout.addWidget(self.path1)
        hlayout.addWidget(self.button3)
        hlayout2.addWidget(self.path2)
        hlayout2.addWidget(self.button4)

        # size window
        width = QWidget()
        height = QWidget()
        width.setLayout(f1)
        height.setLayout(f2)

        hlay.addWidget(width)
        hlay.addWidget(height)

        size_wid = QWidget()
        size_wid.setLayout(hlay)

        # select window
        sel_wid = QWidget()
        sel_wid2 = QWidget()
        sel_wid.setLayout(hlayout)
        sel_wid2.setLayout(hlayout2)

        flayout1.addWidget(sel_wid)
        flayout2.addWidget(sel_wid2)
        flayout1.addWidget(self.edit1)
        flayout2.addWidget(self.edit2)

        fwidget = QWidget()
        fwidget2 = QWidget()

        fwidget.setLayout(flayout1)
        fwidget2.setLayout(flayout2)

        title = QLabel("GCP SELECTOR")
        title.setFont(QFont('Times', 11, QFont.Bold))
        subtitle = QLabel("This program is used for choosing ground control point. ")
        subtitle.setFont(QFont('Times', 9))
        subtitle2 = QLabel("Please modify width and height if images needs to be ")
        subtitle2.setFont(QFont('Times', 9))
        subtitle3 = QLabel("resized when matching features.")
        subtitle3.setFont(QFont('Times', 9))
        layout.addWidget(title, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(subtitle, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(subtitle2, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(subtitle3, alignment=QtCore.Qt.AlignCenter)

        layout.addWidget(size_wid)
        layout.addWidget(fwidget)
        layout.addWidget(fwidget2)

        hlayout3 = QHBoxLayout()
        hlayout3.addWidget(self.button2)
        hlayout3.addWidget(self.button1)

        wid = QWidget()
        wid.setLayout(hlayout3)

        # Add author information to the vertical layout
        label4 = QLabel("Author: Mochuan Zhan", alignment=QtCore.Qt.AlignRight)
        label5 = QLabel("Email: mochuan.zhan@postgrad.manchester.ac.uk", alignment=QtCore.Qt.AlignRight)

        layout.addWidget(wid)
        layout.addWidget(label4)
        layout.addWidget(label5)

        # button click event
        self.button1.clicked.connect(self.save_txt)
        self.button2.clicked.connect(lambda: self.onClickButton())
        self.button3.clicked.connect(self.choose_file_1)
        self.button4.clicked.connect(self.choose_file_2)

        self.setLayout(layout)
        self.show()

    def onClickButton(self):
        sender = self.sender()
        clickEvent = sender.text()
        imgType_list = {'jpg, ''bmp', 'png', 'jpeg', 'jfif'}
        W = self.w.text()
        H = self.h.text()

        if clickEvent == 'Select GCP' and (self.flag is False):
            # Check if edit boxes are empty
            if (self.edit1.toPlainText() is not '') | (self.edit2.toPlainText() is not ''):
                reply = QMessageBox.information(self, 'Notice',
                                                'Current record will be removed, are you sure to reselect?',
                                                QMessageBox.Ok, QMessageBox.Cancel)
                if reply == QMessageBox.Ok:
                    self.edit1.setPlainText('')
                    self.edit2.setPlainText('')

            # check whether path1 and path2 are selected
            if (self.path1.text() == '') | (self.path2.text() == ''):
                QMessageBox.information(self, 'Notice', 'Please select exact 2 image files', QMessageBox.Ok)
            # check if two selected files are images
            elif imghdr.what(self.path1.text()) not in imgType_list:
                QMessageBox.information(self, 'Notice', 'Please select only image files', QMessageBox.Ok)
            elif imghdr.what(self.path2.text()) not in imgType_list:
                QMessageBox.information(self, 'Notice', 'Please select only image files', QMessageBox.Ok)
            elif (W == '') ^ (H == ''):
                QMessageBox.information(self, 'Notice', 'Please input correct W and H for image1 to resize!', QMessageBox.Ok)
            else:
                if not self.flag:
                    self.create_tk()
                    self.flag = True
                self.select_point(W, H)

    def select_point(self, W, H):
        img1 = cv2.imread(self.path1.text())
        if W != '' and H != '':
            img1 = cv2.resize(img1, (int(W), int(H)))
        img2 = cv2.imread(self.path2.text())
        cv2.namedWindow('img1', flags=cv2.WINDOW_NORMAL)
        cv2.resizeWindow('img1', 800, 600)
        cv2.namedWindow('img2', flags=cv2.WINDOW_NORMAL)
        cv2.resizeWindow('img2', 800, 600)
        while self.flag:
            cv2.imshow('img1', img1)
            cv2.imshow('img2', img2)
            cv2.setMouseCallback('img1', on_left_click_1, img1)
            cv2.setMouseCallback('img2', on_left_click_2, img2)
            # add magnifier
            cv2.waitKey(5)
            self.magnifier()
            # wait key to quit
            key = cv2.waitKey(5) & 0xFF
            if key == ord('q'):
                self.root.destroy()
                self.flag = False
                break
            elif cv2.getWindowProperty('img1', cv2.WND_PROP_VISIBLE) < 1:
                self.root.destroy()
                self.flag = False
                break
            elif cv2.getWindowProperty('img2', cv2.WND_PROP_VISIBLE) < 1:
                self.root.destroy()
                self.flag = False
                break
        cv2.destroyAllWindows()

    def add_coord_1(self, coord):
        content = self.edit1.toPlainText()
        if content != '':
            content = content + '\n' + coord
        else:
            content = coord
        self.edit1.setPlainText(content)

    def add_coord_2(self, coord):
        content = self.edit2.toPlainText()
        if content != '':
            content = content + '\n' + coord
        else:
            content = coord
        self.edit2.setPlainText(content)

    def magnifier(self):
        global immg  # [2]
        x, y = pag.position()
        # add offset
        x = x + 20
        y = y + 12
        xx = ImageGrab.grab((x - 50, y - 30, x + 50, y + 30))
        xxx = xx.resize((500, 300))
        immg = ImageTk.PhotoImage(xxx)  # full screen grab
        self.canvas.create_image(200, 120, image=immg)  # [4]
        self.canvas.create_line(0, 60, 200, 60, dash=(5, 2), fill='white')
        self.canvas.create_line(100, 0, 100, 120, dash=(5, 2), fill='white')
        self.root.geometry("200x120+{}+{}".format(x + 50, y + 30))  # [5]
        self.root.update()

    def save_txt(self):
        if not self.flag:
            txt = self.text + '\n'
            list1 = self.edit1.toPlainText().splitlines()
            list2 = self.edit2.toPlainText().splitlines()
            if len(list1) == 0 | len(list2) == 0:
                reply = QMessageBox.information(self, 'Notice', 'No points selected!',
                                                QMessageBox.Ok)
            else:
                for coord in list1:
                    txt = txt + 'GCP,1,' + coord + '\n'

                for coord in list2:
                    txt = txt + 'GCP,2,' + coord + '\n'

                filepath, type = QFileDialog.getSaveFileName(self, "Save cfg", "/", 'cfg(*.cfg)')
                if filepath != '':
                    file = open(filepath, 'w')
                    print(filepath)
                    file.write(txt)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet("QPushButton { padding: 2ex;}")
    ex = App()
    sys.exit(app.exec_())
