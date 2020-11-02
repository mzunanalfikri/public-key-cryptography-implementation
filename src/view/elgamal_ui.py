import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from controller import ElGamal, ElGamalKey
from .helper_ui import spawnDialogWindow


class ElGamalUI:
    def __init__(self):
        self.egKey = ElGamalKey(None, None)
        self.pt = None
        self.ct = None

    def setupUIElGamal(self):
        # key
        self.egGenKeyBtn.clicked.connect(self.egGenerateKey)
        self.egPubLoadBtn.clicked.connect(self.egLoadPublicKey)
        self.egPriLoadBtn.clicked.connect(self.egLoadPrivateKey)
        # encryption
        self.egEncFileInpPathBtn.clicked.connect(self.egSelectPlaintextFile)
        self.egEncryptBtn.clicked.connect(self.egEncrypt)
        self.egSaveCtBtn.clicked.connect(self.egSaveCiphertext)
        # decryption
        self.egDecFileInpPathBtn.clicked.connect(self.egSelectCiphertextFile)
        self.egDecryptBtn.clicked.connect(self.egDecrypt)
        self.egSavePtBtn.clicked.connect(self.egSavePlaintext)

    # handler methods
    def egGenerateKey(self):
        self.egKey = ElGamal.generate_key_pair()
        self.egUpdatePubKeyUI()
        self.egUpdatePriKeyUI()

    def egLoadPublicKey(self):
        fileName, _ = QFileDialog.getOpenFileName(None, 'Load Public Key', '', 'PublicKey (*.pub)')
        if fileName:
            try:
                self.egKey.load_public_key(fileName)
            except Exception as e:
                print('Error:', e)
            else:
                self.egUpdatePubKeyUI()

    def egLoadPrivateKey(self):
        fileName, _ = QFileDialog.getOpenFileName(None, 'Load Private Key', '', 'PrivateKey (*.pri)')
        if fileName:
            try:
                self.egKey.load_private_key(fileName)
            except Exception as e:
                print('Error:', e)
            else:
                self.egUpdatePriKeyUI()

    def egSelectPlaintextFile(self):
        fileName, _ = QFileDialog.getOpenFileName(None, 'Select Plaintext File', '', 'All Files (*.*)')
        if fileName:
            self.egEncFileInpPathInp.setText(fileName)

    def egEncrypt(self):
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
        self.ct = ElGamal.encrypt(pt, self.egKey.public)
        lsA, lsB = self.ct
        self.egEncCtAOut.setPlainText(','.join(list(map(str, lsA))))
        self.egEncCtBOut.setPlainText(','.join(list(map(str, lsB))))

    def egSaveCiphertext(self):
        if self.ct is None:
            print('Ciphertext is empty!')
            return
        fileName, _ = QFileDialog.getSaveFileName(None, 'Save Ciphertext', 'ciphertext.txt', 'Txt Files (*.txt)')
        if fileName:
            lsA, lsB = self.ct
            with open(fileName, 'w') as f:
                f.write('a=' + ','.join(list(map(str, lsA))) + '\n')
                f.write('b=' + ','.join(list(map(str, lsB))) + '\n')

    def egSelectCiphertextFile(self):
        fileName, _ = QFileDialog.getOpenFileName(None, 'Select Ciphertext File', '', 'All Files (*.*)')
        if fileName:
            self.egDecFileInpPathInp.setText(fileName)

    def egDecrypt(self):
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
        self.pt = ElGamal.decrypt((lsA, lsB), self.egKey.private)
        self.egDecPtOut.setPlainText(self.pt.decode('latin-1'))

    def egSavePlaintext(self):
        if self.pt is None:
            print('Plaintext is empty!')
            return
        fileName, _ = QFileDialog.getSaveFileName(None, 'Save Plaintext', 'plaintext.txt', 'Txt Files (*.txt)')
        if fileName:
            with open(fileName, 'wb') as f:
                f.write(self.pt)

    # helper methods
    def egUpdatePubKeyUI(self):
        self.egPubYInp.setText(str(self.egKey.public.y))
        self.egPubGInp.setText(str(self.egKey.public.g))
        self.egPubPInp.setText(str(self.egKey.public.p))

    def egUpdatePriKeyUI(self):
        self.egPriXInp.setText(str(self.egKey.private.x))
        self.egPriPInp.setText(str(self.egKey.private.p))
