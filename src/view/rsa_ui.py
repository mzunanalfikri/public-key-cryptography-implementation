import os
import sys
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsPixmapItem, QGraphicsScene, QErrorMessage, QMessageBox
from PyQt5.QtGui import QPixmap

from controller import RSA


class RSAUI:
    def __init__(self):
        self.pt_path = ''
        self.ct_path = ''
        self.rsa = RSA()

    def setupUIRSA(self):
        self.button_generate_key.clicked.connect(self.generate_key)
        self.button_save_key.clicked.connect(self.save_key)
        self.button_e_load_file.clicked.connect(self.load_pt)
        self.button_d_load_file.clicked.connect(self.load_ct)
        self.button_load_pub_key.clicked.connect(self.load_public_key)
        self.button_load_pri_key.clicked.connect(self.load_private_key)
        self.button_enkripsi.clicked.connect(self.encrypt)
        self.button_dekripsi.clicked.connect(self.decrypt)

    def generate_key(self):
        self.rsa.generate_key()
        self.n_key.setText(str(self.rsa.n))
        self.e_key.setText(str(self.rsa.e))
        self.d_key.setText(str(self.rsa.d))

    def save_key(self):
        try:
            n = int(self.n_key.text())
            e = int(self.e_key.text())
            d = int(self.d_key.text())
            name = QFileDialog.getSaveFileName(self, 'Save File')
            self.rsa.save_key(name[0], e, n, d)
        except:
            self.warning_msg("Wrong Key!", "Key must be integer")

    def warning_msg(self,title, msg):
        temp = msg
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText(str(title))
        msg.setInformativeText(temp)
        msg.exec_()

    def load_pt(self):
        fname = QFileDialog().getOpenFileName(None, "Load Plaintext", "", "Allfiles (*.txt)")
        self.pt_path = (fname[0])
        self.refresh()

    def load_ct(self):
        fname = QFileDialog().getOpenFileName(None, "Load Ciphertext", "", "Text (*.txt)")
        self.ct_path = (fname[0])
        self.refresh()

    def load_public_key(self):
        fname = QFileDialog().getOpenFileName(None, "Load Public Key", "", "PublicKey (*.pub)")
        f = open(fname[0], "r")
        key = f.read().split(" ")
        f.close()
        self.n_key.setText(key[1])
        self.e_key.setText(key[0])

    def load_private_key(self):
        fname = QFileDialog().getOpenFileName(None, "Load Private Key", "", "PrivateKey (*.pri)")
        f = open(fname[0], "r")
        key = f.read().split(" ")
        f.close()
        self.n_key.setText(key[1])
        self.d_key.setText(key[0])

    def refresh(self):
        self.e_file_name.setText(self.pt_path)
        self.d_file_name.setText(self.ct_path)

    def encrypt(self):
        if (self.n_key.text() == "" or self.e_key.text() == "" ):
            self.warning_msg("Wrong Key!", "Key must be filled!")
            return
        print(self.e_plaintext.toPlainText())
        if (not((self.e_plaintext.toPlainText() == "") ^ (self.pt_path == ''))):
            self.warning_msg("Wrong Plaintext!", "Plaintext mus be loaded from file or writen in textbox")

        if (self.e_plaintext.toPlainText() != ''):
            pt = bytes(self.e_plaintext.toPlainText(), 'utf-8')
            ct = self.rsa.encrypt(pt, int(self.e_key.text()), int(self.n_key.text()))
            self.e_ciphertext.setPlainText(' '.join(ct))
        else:
            f = open(self.pt_path, "rb")
            pt = f.read()
            f.close()
            ct = self.rsa.encrypt(pt, int(self.e_key.text()), int(self.n_key.text()))
            fname = QFileDialog.getSaveFileName(self, 'Save File')
            f = open(fname[0] + ".txt", "w")
            f.write(' '.join(ct))
            f.close()
            self.pt_path = ""
            self.refresh()

    def decrypt(self):
        if (self.n_key.text() == "" or self.d_key.text() == "" ):
            self.warning_msg("Wrong Key!", "Key must be filled!")
            return

        if (not((self.d_ciphertext.toPlainText() == "") ^ (self.ct_path == ''))):
            self.warning_msg("Wrong Ciphertext!", "Ciphertext mus be loaded from file or writen in textbox")

        if (self.d_ciphertext.toPlainText() != ''):
            load = self.d_ciphertext.toPlainText().split(" ")
            ct = [int(i) for i in load]
            print("hasil ct" , ct)
            pt = self.rsa.decrypt(ct, int(self.d_key.text()), int(self.n_key.text()))
            print("hasil pt = ", pt)
            self.d_plaintext.setPlainText(pt.decode())
        else:
            f = open(self.ct_path, "r")
            temp = f.read().split(" ")
            f.close()
            ct = [int(i) for i in temp]
            pt = self.rsa.decrypt(ct, int(self.d_key.text()), int(self.n_key.text()))
            fname = QFileDialog.getSaveFileName(self, 'Save File')
            f = open(fname[0] + ".txt", "wb")
            f.write(pt)
