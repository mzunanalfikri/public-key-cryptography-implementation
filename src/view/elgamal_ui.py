import os
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from controller import ElGamal, ElGamalKey, ElGamalPublicKey, ElGamalPrivateKey
from .helper_ui import spawnDialogWindow


class ElGamalUI:
    def setupUIElGamal(self):
        # key
        self.egGenKeyBtn.clicked.connect(self.egGenerateKey)
        self.egPubLoadBtn.clicked.connect(self.egLoadPublicKey)
        self.egPriLoadBtn.clicked.connect(self.egLoadPrivateKey)
        self.egSavePubKeyBtn.clicked.connect(self.egSavePublicKey)
        self.egSavePriKeyBtn.clicked.connect(self.egSavePrivateKey)
        # encryption
        self.egEncFileInpPathBtn.clicked.connect(self.egSelectPlaintextFile)
        self.egEncryptBtn.clicked.connect(self.egEncrypt)
        # decryption
        self.egDecFileInpPathBtn.clicked.connect(self.egSelectCiphertextFile)
        self.egDecryptBtn.clicked.connect(self.egDecrypt)

    # handler methods
    def egGenerateKey(self):
        key = ElGamal.generate_key_pair()
        self.egUpdatePubKeyUI(key.public)
        self.egUpdatePriKeyUI(key.private)

    def egLoadPublicKey(self):
        fileName, _ = QFileDialog.getOpenFileName(None, 'Load Public Key', '', 'PublicKey (*.pub)')
        if fileName:
            try:
                key = ElGamalKey.from_file(fileName, None)
            except Exception as e:
                spawnDialogWindow('Error Happened', str(e), type='Warning')
            else:
                self.egUpdatePubKeyUI(key.public)

    def egLoadPrivateKey(self):
        fileName, _ = QFileDialog.getOpenFileName(None, 'Load Private Key', '', 'PrivateKey (*.pri)')
        if fileName:
            try:
                key = ElGamalKey.from_file(None, fileName)
            except Exception as e:
                spawnDialogWindow('Error Happened', str(e), type='Warning')
            else:
                self.egUpdatePriKeyUI(key.private)

    def egSavePublicKey(self):
        public_key = self.egGetPublicKey()
        if public_key is None:
            return
        key = ElGamalKey(public_key, None)
        fileName, _ = QFileDialog.getSaveFileName(None, 'Save Public Key', 'key.pub', 'PublicKey Files (*.pub)')
        if fileName:
            try:
                key.save_public_key(fileName)
            except Exception as e:
                spawnDialogWindow('Error Happened', str(e), type='Warning')

    def egSavePrivateKey(self):
        private_key = self.egGetPrivateKey()
        if private_key is None:
            return
        key = ElGamalKey(None, private_key)
        fileName, _ = QFileDialog.getSaveFileName(None, 'Save Private Key', 'key.pri', 'PrivateKey Files (*.pri)')
        if fileName:
            try:
                key.save_private_key(fileName)
            except Exception as e:
                spawnDialogWindow('Error Happened', str(e), type='Warning')

    def egSelectPlaintextFile(self):
        fileName, _ = QFileDialog.getOpenFileName(None, 'Select Plaintext File', '', 'All Files (*.*)')
        if fileName:
            self.egEncFileInpPathInp.setText(fileName)

    def egEncrypt(self):
        # get public key
        public_key = self.egGetPublicKey()
        if public_key is None:
            return
        # check input
        if not((self.egEncFileInpPathInp.text() != '') ^ (self.egEncPtInp.toPlainText() != '')):
            spawnDialogWindow('Encrypt Failed', 'Please insert either file input path or plaintext form', type='Warning')
            return
        # get plaintext
        if self.egEncFileInpPathInp.text():
            if os.path.isfile(self.egEncFileInpPathInp.text()):
                with open(self.egEncFileInpPathInp.text(), 'rb') as f:
                    pt = f.read()
            else:
                spawnDialogWindow('Open File', self.egEncFileInpPathInp.text(), subtext='File not found!', type='Warning')
                return
        else:
            pt = bytes(self.egEncPtInp.toPlainText(), 'latin-1')
        # encrypt
        try:
            st = time.time()
            ct = ElGamal.encrypt(pt, public_key)
            ed = time.time()
        except Exception as e:
            spawnDialogWindow('Error Happened', str(e), type='Warning')
            return
        # output
        lsA, lsB = ct
        if self.egEncFileInpPathInp.text():
            fileName, _ = QFileDialog.getSaveFileName(None, 'Save Ciphertext', 'ciphertext.txt', 'Txt Files (*.txt)')
            if fileName:
                with open(fileName, 'w') as f:
                    f.write('a=' + ','.join(list(map(str, lsA))) + '\n')
                    f.write('b=' + ','.join(list(map(str, lsB))) + '\n')
                self.egEncCtAOut.clear()
                self.egEncCtBOut.clear()
        else:
            self.egEncCtAOut.setPlainText(','.join(list(map(str, lsA))))
            self.egEncCtBOut.setPlainText(','.join(list(map(str, lsB))))
        # summary (time and size, ciphertext size excluding 'a=' and 'b=')
        len_pt = len(pt)
        len_ct = len(','.join(list(map(str, lsA)))) + len(','.join(list(map(str, lsB))))
        msg = 'Time: ' + str(ed - st) + ' sekon\nPlaintext: ' + str(len_pt) + ' bytes\nCiphertext: ' + str(len_ct) + ' bytes'
        spawnDialogWindow('Encryption Succeed', msg, type='Information')

    def egSelectCiphertextFile(self):
        fileName, _ = QFileDialog.getOpenFileName(None, 'Select Ciphertext File', '', 'All Files (*.*)')
        if fileName:
            self.egDecFileInpPathInp.setText(fileName)

    def egDecrypt(self):
        # get private key
        private_key = self.egGetPrivateKey()
        if private_key is None:
            return
        # check input
        if (self.egDecFileInpPathInp.text() == '') and (self.egDecCtAInp.toPlainText() == '' or self.egDecCtBInp.toPlainText() == ''):
            spawnDialogWindow('Decrypt Failed', 'Please insert either file input path or ciphertext (a and b) form', type='Warning')
            return
        if (self.egDecFileInpPathInp.text() != '') and (self.egDecCtAInp.toPlainText() != '' or self.egDecCtBInp.toPlainText() != ''):
            spawnDialogWindow('Decrypt Failed', 'Please insert either file input path or ciphertext (a and b) form', type='Warning')
            return
        # get plaintext
        if self.egDecFileInpPathInp.text():
            if os.path.isfile(self.egDecFileInpPathInp.text()):
                with open(self.egDecFileInpPathInp.text(), 'r') as f:
                    lsA = list(map(int, f.readline().strip('\n').split('=')[1].split(',')))
                    lsB = list(map(int, f.readline().strip('\n').split('=')[1].split(',')))
            else:
                spawnDialogWindow('Open File', self.egDecFileInpPathInp.text(), subtext='File not found!', type='Warning')
                return
        else:
            lsA = list(map(int, self.egDecCtAInp.toPlainText().split(',')))
            lsB = list(map(int, self.egDecCtBInp.toPlainText().split(',')))
        # decrypt
        try:
            st = time.time()
            pt = ElGamal.decrypt((lsA, lsB), private_key)
            ed = time.time()
        except Exception as e:
            spawnDialogWindow('Error Happened', str(e), type='Warning')
            return
        # output
        if self.egDecFileInpPathInp.text():
            fileName, _ = QFileDialog.getSaveFileName(None, 'Save Plaintext', 'plaintext.txt', 'All Files (*.*)')
            if fileName:
                with open(fileName, 'wb') as f:
                    f.write(pt)
                self.egDecPtOut.clear()
        else:
            self.egDecPtOut.setPlainText(pt.decode('latin-1'))
        # summary (time and size, ciphertext size excluding 'a=' and 'b=')
        len_ct = len(','.join(list(map(str, lsA)))) + len(','.join(list(map(str, lsB))))
        len_pt = len(pt)
        msg = 'Time: ' + str(ed - st) + ' sekon\nCiphertext: ' + str(len_ct) + ' bytes\nPlaintext: ' + str(len_pt) + ' bytes'
        spawnDialogWindow('Decryption Succeed', msg, type='Information')

    # helper methods
    def egUpdatePubKeyUI(self, public_key):
        self.egPubYInp.setText(str(public_key.y))
        self.egPubGInp.setText(str(public_key.g))
        self.egPubPInp.setText(str(public_key.p))

    def egUpdatePriKeyUI(self, private_key):
        self.egPriXInp.setText(str(private_key.x))
        self.egPriPInp.setText(str(private_key.p))

    def egGetPublicKey(self):
        if not (self.egPubYInp.text() and self.egPubGInp.text() and self.egPubPInp.text()):
            spawnDialogWindow('Invalid Public Key', 'Public key form is not all filled', type='Warning')
            return None
        try:
            y = int(self.egPubYInp.text())
            g = int(self.egPubGInp.text())
            p = int(self.egPubPInp.text())
        except Exception as e:
            spawnDialogWindow('Invalid Public Key', str(e), type='Warning')
            return None
        else:
            return ElGamalPublicKey(y, g, p)

    def egGetPrivateKey(self):
        if not (self.egPriXInp.text() and self.egPriPInp.text()):
            spawnDialogWindow('Invalid Private Key', 'Private key form is not all filled', type='Warning')
            return None
        try:
            x = int(self.egPriXInp.text())
            p = int(self.egPriPInp.text())
        except Exception as e:
            spawnDialogWindow('Invalid Private Key', str(e), type='Warning')
            return None
        else:
            return ElGamalPrivateKey(x, p)
