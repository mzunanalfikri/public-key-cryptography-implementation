import collections
import random
from Cryptodome.Util.number import getPrime


pack_key_value = lambda k, v: str(k) + '=' + str(v) + '\n'
unpack_key_value = lambda line: int(line.strip('\n').split('=')[1])

ElGamalPublicKey = collections.namedtuple('ElGamalPublicKey', ['y', 'g', 'p'])
ElGamalPrivateKey = collections.namedtuple('ElGamalPrivateKey', ['x', 'p'])


class ElGamalKey:
    def __init__(self, y, g, x, p):
        self.public = ElGamalPublicKey(y, g, p)
        self.private = ElGamalPrivateKey(x, p)

    def to_file(self, public_key_filename: str, private_key_filename: str):
        self.save_public_key(public_key_filename)
        self.save_private_key(private_key_filename)

    def save_public_key(self, public_key_filename: str):
        with open(public_key_filename, 'w') as f:
            for k in self.public._fields:
                f.write(pack_key_value(k, getattr(self.public, k)))

    def save_private_key(self, private_key_filename: str):
        with open(private_key_filename, 'w') as f:
            for k in self.private._fields:
                f.write(pack_key_value(k, getattr(self.private, k)))

    @classmethod
    def from_file(cls, public_key_filename: str, private_key_filename: str):
        # load public key
        with open(public_key_filename, 'r') as f:
            y = unpack_key_value(f.readline())
            g = unpack_key_value(f.readline())
            p = unpack_key_value(f.readline())
        # load private key
        with open(private_key_filename, 'r') as f:
            x = unpack_key_value(f.readline())
            assert p == unpack_key_value(f.readline())  # assert p value is the same in .pub and .pri file
        # return new class instance
        return cls(y, g, x, p)


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
    # save
    key.to_file('test.pub', 'test.pri')
    # load
    new_key = ElGamalKey.from_file('test.pub', 'test.pri')
    # check
    assert key.public == new_key.public
    assert key.private == new_key.private
    print('ok')

    # TEST enc-dec
    # for i in range(1000):
    #     pt = random.randint(0, key.public.p - 1)
    #     print(pt)
    #     ct = ElGamal.encrypt(pt, key.public)
    #     new_pt = ElGamal.decrypt(ct, key.private)
    #     assert pt == new_pt
    #     print('ok')
