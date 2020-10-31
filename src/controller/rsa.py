from sympy import randprime
import random
from util import plaintext_to_block, block_to_plaintext

class RSA:
    def __init__(self, key_size=10):
        self.key_size = key_size
        self.e = None
        self.d = None
        self.n = None
        self.generate_key()

    def gcd(self, a, b):
        while a != 0:
            a, b = b % a, a
        return b

    def mod_inverse(self, a, m): 
        a = a % m
        for x in range(1, m) : 
            if ((a * x) % m == 1) : 
                return x 
        return 1

    def generate_key(self):
        self.p = randprime(2**(self.key_size - 1), 2**self.key_size)
        self.q = randprime(2**(self.key_size - 1), 2**self.key_size)
        self.n = self.p*self.q
        self.toitent_euler = (self.p - 1) * (self.q - 1)

        while True:
            self.e = random.randrange(2 ** (self.key_size - 1), 2 ** self.key_size)
            if (self.gcd(self.e, self.toitent_euler) == 1):
                break
        self.d = pow(self.e, -1, self.toitent_euler)
        print(self.p)
        print(self.q)
        print("e : ", self.e)
        print("d :", self.d)
        print("panjang e :", len(str(self.e)))
        print("panjang d :", len(str(self.d)))

    def save_key(self, path):
        pub = open(path+ "rsa.pub", "w")
        pub.write(str(self.e) + " " + str(self.n))
        pub.close()
        pri = open(path + "rsa.pri", "w")
        pri.write(str(self.d) + " " + str(self.n))
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
        print("pt : ", pt)
        res = []
        for block in pt:
            res.append(pow(block, e, n))
        print(res)
        return res
    
    def decrypt(self, ciphertext_block, d, n):
        # TODO : load ke block
        res = []
        for block in ciphertext_block:
            res.append(pow(block, d, n))
        ct = block_to_plaintext(res, len(str(n))-1 )
        print(ct)

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

