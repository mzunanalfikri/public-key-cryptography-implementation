from sympy import randprime
import random
from util import plaintext_to_block, block_to_plaintext

class RSA:
    def __init__(self, key_size=180):
        self.key_size = key_size
        self.e = None
        self.d = None
        self.n = None
        # self.generate_key()

    def gcd(self, a, b):
        while a != 0:
            a, b = b % a, a
        return b

    def extended_gcd(self, a, b):
        if a == 0:  # base
            return (b, 0, 1)
        g, y, x = self.extended_gcd(b % a, a)  # recc
        return (g, x - (b // a) * y, y)

    def mod_inverse(self, a, m):
        g, x, _ = self.extended_gcd(a, m)
        if g != 1:  # not exists
            raise Exception('Modular inverse not exists!')
        return x % m

    def generate_key(self):
        self.p = randprime(2**(self.key_size - 1), 2**self.key_size)
        self.q = randprime(2**(self.key_size - 1), 2**self.key_size)
        self.n = self.p*self.q
        self.toitent_euler = (self.p - 1) * (self.q - 1)

        while True:
            self.e = random.randrange(2 ** (self.key_size - 1), 2 ** self.key_size)
            if (self.gcd(self.e, self.toitent_euler) == 1):
                break
        # self.d = pow(self.e, -1, self.toitent_euler)
        self.d = self.mod_inverse(self.e, self.toitent_euler)
        print(self.p)
        print(self.q)
        print("e : ", self.e)
        print("d :", self.d)
        print("panjang e :", len(str(self.e)))
        print("panjang d :", len(str(self.d)))

    def save_key(self, path, e, n, d):
        pub = open(path+ ".pub", "w")
        pub.write(str(e) + " " + str(n))
        pub.close()
        pri = open(path + ".pri", "w")
        pri.write(str(d) + " " + str(n))
        pri.close()

    def load_public_key(self, path):
        f = open(path, "r")
        pub = f.read().split(" ")
        f.close()
        assert len(pub) == 2
        self.e = int(pub[0])
        self.n = int(pub[1])
        # print("e : ", self.e, "n :", self.n, type(self.e), type(self.n))

    def load_private_key(self, path):
        f = open(path, "r")
        pri = f.read().split(" ")
        f.close()
        assert len(pri) == 2
        self.d = int(pri[0])
        self.n = int(pri[1])
        # print("d : ", self.d, "n :", self.n, type(self.d), type(self.n))

    def encrypt(self, plaintext, e, n):
        # TODO : load ke block
        pt = plaintext_to_block(plaintext, len(str(n)) - 1)
        res = []
        for block in pt:
            res.append(str(pow(block, e, n)))
        print("Hasil dari enkripsi :", res)
        return res

    def decrypt(self, ciphertext_block, d, n):
        # TODO : load ke block
        res = []
        for block in ciphertext_block:
            res.append(pow(block, d, n))
        print("hasil dari dekripsi :", res)
        ct = block_to_plaintext(res, len(str(n))-1 )
        return (ct)

if __name__ == "__main__":
    rsa = RSA()
    # rsa.load_public_key("rsa.pub")
    # rsa.load_private_key("rsa.pri")
    f = open("test.txt", "rb")
    pt = (f.read())
    f.close()
    ct = rsa.encrypt(pt, rsa.e, rsa.n)
    rsa.decrypt(ct, rsa.d,rsa.n)
    # temp = rsa.encrypt(999)
    # rsa.decrypt(temp)
