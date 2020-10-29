import os
from PyQt5.uic import loadUi
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from controller import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi(os.path.join(os.getcwd(), "view", "main_window.ui"), self)
        # change page helper
        self.changePage = lambda idx: self.stackedWidget.setCurrentIndex(idx)

    def setupUI(self):
        # # define event connection here, for example:
        # self.imageButton.clicked.connect(self.imageButtonClickedHandler)
        # self.audioButton.clicked.connect(self.audioButtonClickedHandler)
        # self.videoButton.clicked.connect(self.videoButtonClickedHandler)
        pass

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
