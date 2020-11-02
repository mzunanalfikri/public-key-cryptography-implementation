import os
from enum import IntEnum
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from controller import *
from .rsa_ui import RSAUI
from .elgamal_ui import ElGamalUI
from .diffie_hellman_ui import DiffieHellmanUI


class PageIdx(IntEnum):
    MAIN_MENU = 0
    RSA_PAGE = 1
    ELGAMAL_PAGE = 2
    DH_PAGE = 3


class MainWindow(QMainWindow, RSAUI, ElGamalUI, DiffieHellmanUI):
    def __init__(self):
        # call parents constructor
        # super(MainWindow, self).__init__()
        QMainWindow.__init__(self)
        RSAUI.__init__(self)
        ElGamalUI.__init__(self)
        DiffieHellmanUI.__init__(self)

        # load ui
        loadUi(os.path.join(os.getcwd(), "view", "main_window.ui"), self)
        # change page helper
        self.changePage = lambda idx: self.stackedWidget.setCurrentIndex(idx)
        # setup ui
        self.setupUI()

    def setupUI(self):
        # main menu page
        self.rsaPageBtn.clicked.connect(lambda: self.changePage(PageIdx.RSA_PAGE))
        self.elgamalPageBtn.clicked.connect(lambda: self.changePage(PageIdx.ELGAMAL_PAGE))
        self.dhPageBtn.clicked.connect(lambda: self.changePage(PageIdx.DH_PAGE))
        self.exitBtn.clicked.connect(lambda: self.close())
        # rsa page
        self.setupUIRSA()
        self.rsaBackBtn.clicked.connect(lambda: self.changePage(PageIdx.MAIN_MENU))
        # elgamal page
        self.setupUIElGamal()
        self.egBackBtn.clicked.connect(lambda: self.changePage(PageIdx.MAIN_MENU))
        # diffie hellman page
        self.setupUIDiffieHellman()
        self.dhBackBtn.clicked.connect(lambda: self.changePage(PageIdx.MAIN_MENU))
