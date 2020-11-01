from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from controller import ElGamal, ElGamalKey


class ElGamalUI:
    def __init__(self):
        self.egKey = ElGamalKey(None, None)

    def setupUIElGamal(self):
        # key
        self.egGenKeyBtn.clicked.connect(self.egGenerateKey)
        self.egPubLoadBtn.clicked.connect(self.egLoadPublicKey)
        self.egPriLoadBtn.clicked.connect(self.egLoadPrivateKey)
        # encryption
        self.egEncryptBtn.clicked.connect(self.egEncrypt)
        # decryption
        self.egDecryptBtn.clicked.connect(self.egDecrypt)

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

    def egEncrypt(self):
        pt = bytes(self.egEncPtInp.toPlainText(), 'utf-8')
        self.ct = ElGamal.encrypt(pt, self.egKey.public)
        lsA, lsB = self.ct
        self.egEncCtAOut.setPlainText(','.join(list(map(str, lsA))))
        self.egEncCtBOut.setPlainText(','.join(list(map(str, lsB))))

    def egDecrypt(self):
        lsA = list(map(int, self.egDecCtAInp.toPlainText().split(',')))
        lsB = list(map(int, self.egDecCtBInp.toPlainText().split(',')))
        self.pt = ElGamal.decrypt((lsA, lsB), self.egKey.private)
        self.egDecPtOut.setPlainText(self.pt.decode())

    # helper methods
    def egUpdatePubKeyUI(self):
        self.egPubYInp.setText(str(self.egKey.public.y))
        self.egPubGInp.setText(str(self.egKey.public.g))
        self.egPubPInp.setText(str(self.egKey.public.p))

    def egUpdatePriKeyUI(self):
        self.egPriXInp.setText(str(self.egKey.private.x))
        self.egPriPInp.setText(str(self.egKey.private.p))
