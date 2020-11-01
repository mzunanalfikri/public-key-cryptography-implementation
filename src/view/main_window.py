import os
from enum import IntEnum
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from controller import *
from .rsa_ui import RSAUI
from .elgamal_ui import ElGamalUI


class PageIdx(IntEnum):
    MAIN_MENU = 0
    RSA_PAGE = 1
    ELGAMAL_PAGE = 2
    DH_PAGE = 3


class MainWindow(QMainWindow, RSAUI, ElGamalUI):
    def __init__(self):
        # call parents constructor
        # super(MainWindow, self).__init__()
        QMainWindow.__init__(self)
        RSAUI.__init__(self)
        ElGamalUI.__init__(self)
        # load ui
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
        # rsa page
        self.setupUIRSA()
        # elgamal page
        self.setupUIElGamal()
        self.egBackBtn.clicked.connect(lambda: self.changePage(PageIdx.MAIN_MENU))
