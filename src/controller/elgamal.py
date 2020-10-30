import collections
import random
from Cryptodome.Util.number import getPrime


ElGamalPublicKey = collections.namedtuple('ElGamalPublicKey', ['y', 'g', 'p'])
ElGamalPrivateKey = collections.namedtuple('ElGamalPrivateKey', ['x', 'p'])


class ElGamalKey:
    def __init__(self, y, g, x, p):
        self.public = ElGamalPublicKey(y, g, p)
        self.private = ElGamalPrivateKey(x, p)


class ElGamal:
    @staticmethod
    def generate_key_pair():
        p = getPrime(1024)
        g = random.randint(2, p - 1)
        x = random.randint(1, p - 2)
        y = pow(g, x, p)
        return ElGamalKey(y, g, x, p)

    @staticmethod
    def encrypt(pt, public_key: ElGamalPublicKey):
        # init
        # TODO: create message block, remove assertion
        assert 0 <= pt <= (public_key.p - 1)
        m = pt
        # unpack public key
        y, g, p = public_key
        # encrypt
        k = random.randint(1, p - 2)
        a = pow(g, k, p)
        b = (pow(y, k, p) * m) % p
        # return
        return a, b

    @staticmethod
    def decrypt(ct: tuple, private_key: ElGamalPrivateKey):
        # init
        assert len(ct) == 2
        # unpack private key
        x, p = private_key
        # decrypt
        a, b = ct
        inv = pow(a, p - 1 - x, p)
        m = (b * inv) % p
        # return
        # TODO: rebuild pt from appending m blocks
        pt = m
        return pt


if __name__ == '__main__':
    key = ElGamal.generate_key_pair()
    for i in range(1000):
        pt = random.randint(0, key.public.p - 1)
        print(pt)
        ct = ElGamal.encrypt(pt, key.public)
        new_pt = ElGamal.decrypt(ct, key.private)
        assert pt == new_pt
        print('ok')
