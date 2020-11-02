from controller import DiffieHellman


class DiffieHellmanUI:
    def __init__(self):
        pass

    def setupUIDiffieHellman(self):
        self.dhGetSharedKeyBtn.clicked.connect(self.dhStartKeyExchange)

    # handler methods
    def dhStartKeyExchange(self):
        # get input
        inp = self.dhGetInput()
        if inp is None:
            return
        n, g, x, y = inp
        # key exchange
        # d = DiffieHellman(97, 5, 36, 58)
        dh = DiffieHellman(n, g, x, y)
        # output
        self.dhResultOut.clear()
        if self.dhShowStepsCbox.isChecked():
            generator = dh.simulate_key_exchange()
            # Alice and Bob agreed n and g publicly
            n, g = next(generator, None)
            self.dhResultOut.appendPlainText('Alice and Bob agreed n = ' + str(n) + ' and g = ' + str(g))
            self.dhResultOut.appendPlainText('')
            # Alice choose x privately, then calculate and send X to Bob
            x, X = next(generator, None)
            self.dhResultOut.appendPlainText('Step 1')
            self.dhResultOut.appendPlainText('Alice chooses x = ' + str(x))
            self.dhResultOut.appendPlainText('Alice sends X = (g^x) mod n = ' + str(X) + ' to Bob')
            self.dhResultOut.appendPlainText('')
            # Bob choose y privately, then calculate and send Y to Alice
            y, Y = next(generator, None)
            self.dhResultOut.appendPlainText('Step 2')
            self.dhResultOut.appendPlainText('Bob chooses y = ' + str(y))
            self.dhResultOut.appendPlainText('Bob sends Y = (g^y) mod n = ' + str(Y) + ' to Alice')
            self.dhResultOut.appendPlainText('')
            # Alice calculate simetric key K
            KAlice = next(generator, None)
            self.dhResultOut.appendPlainText('Step 3')
            self.dhResultOut.appendPlainText('Alice calculates K = (Y^x) mod n = ' + str(KAlice))
            self.dhResultOut.appendPlainText('')
            # Bob calculate simetric key K
            KBob = next(generator, None)
            self.dhResultOut.appendPlainText('Step 4')
            self.dhResultOut.appendPlainText('Bob calculates K = (X^y) mod n = ' + str(KBob))
            self.dhResultOut.appendPlainText('')
            # Last
            KShared = next(generator, None)
            self.dhResultOut.appendPlainText('Alice and Bob has same simetric key K = ' + str(KShared))
            self.dhResultOut.appendPlainText('')
        else:
            self.dhResultOut.appendPlainText('Key exchange succeed')
            self.dhResultOut.appendPlainText('Alice and Bob got same simetric key K = ' + str(dh.K))

    # helper methods
    def dhGetInput(self):
        if not (self.dhInpNInp.text() and self.dhInpGInp.text() and self.dhInpXInp.text() and self.dhInpYInp.text()):
            spawnDialogWindow('Invalid Input', 'Input form is not all filled', type='Warning')
            return None
        try:
            n = int(self.dhInpNInp.text())
            g = int(self.dhInpGInp.text())
            x = int(self.dhInpXInp.text())
            y = int(self.dhInpYInp.text())
        except Exception as e:
            spawnDialogWindow('Invalid Input', str(e), type='Warning')
            return None
        else:
            return (n, g, x, y)
