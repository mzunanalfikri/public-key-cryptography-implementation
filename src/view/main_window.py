import os
from enum import IntEnum
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from controller import *


class PageIdx(IntEnum):
    MAIN_MENU = 0
    RSA_PAGE = 1
    ELGAMAL_PAGE = 2
    DH_PAGE = 3


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi(os.path.join(os.getcwd(), "view", "main_window.ui"), self)
        # change page helper
        self.changePage = lambda idx: self.stackedWidget.setCurrentIndex(idx)
        # setup ui
        self.setupUI()

    def setupUI(self):
        # # define event connection here, for example:
        # self.imageButton.clicked.connect(self.imageButtonClickedHandler)
        # self.audioButton.clicked.connect(self.audioButtonClickedHandler)
        # self.videoButton.clicked.connect(self.videoButtonClickedHandler)

        # main menu page
        self.rsaPageBtn.clicked.connect(lambda: self.changePage(PageIdx.RSA_PAGE))
        self.elgamalPageBtn.clicked.connect(lambda: self.changePage(PageIdx.ELGAMAL_PAGE))
        self.dhPageBtn.clicked.connect(lambda: self.changePage(PageIdx.DH_PAGE))
        self.exitBtn.clicked.connect(lambda: self.close())

    # Helper methods
    def spawnDialogWindow(self, title, text, subtext="" , type="Information"):
        message = QMessageBox()
        if type == "Question":
            message.setIcon(QMessageBox.Question)
        elif type == "Warning":
            message.setIcon(QMessageBox.Warning)
        elif type == "Critical":
            message.setIcon(QMessageBox.Critical)
        else:
            message.setIcon(QMessageBox.Information)
        message.setWindowTitle(title)
        message.setText(text)
        message.setInformativeText(subtext)
        message.setStandardButtons(QMessageBox.Ok)
        message._exec()
