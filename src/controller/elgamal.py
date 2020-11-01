import collections
import random
from Cryptodome.Util.number import getPrime

from util import plaintext_to_block, block_to_plaintext


pack_key_value = lambda k, v: str(k) + '=' + str(v) + '\n'
unpack_key_value = lambda line: int(line.strip('\n').split('=')[1])

ElGamalPublicKey = collections.namedtuple('ElGamalPublicKey', ['y', 'g', 'p'])
ElGamalPrivateKey = collections.namedtuple('ElGamalPrivateKey', ['x', 'p'])


class ElGamalKey:
    def __init__(self, public_key: ElGamalPublicKey, private_key: ElGamalPrivateKey):
        self.public = public_key
        self.private = private_key

    def set_public_key(self, public_key):
        self.public = public_key

    def set_private_key(self, private_key):
        self.private = private_key

    def to_file(self, public_key_filename: str, private_key_filename: str):
        if public_key_filename is not None:
            self.save_public_key(public_key_filename)
        if private_key_filename is not None:
            self.save_private_key(private_key_filename)

    def save_public_key(self, public_key_filename: str):
        if self.public is None:
            raise Exception('Public key not exists!')
        with open(public_key_filename, 'w') as f:
            for k in self.public._fields:
                f.write(pack_key_value(k, getattr(self.public, k)))

    def save_private_key(self, private_key_filename: str):
        if self.private is None:
            raise Exception('Private key not exists!')
        with open(private_key_filename, 'w') as f:
            for k in self.private._fields:
                f.write(pack_key_value(k, getattr(self.private, k)))

    def load_public_key(self, public_key_filename: str):
        with open(public_key_filename, 'r') as f:
            y = unpack_key_value(f.readline())
            g = unpack_key_value(f.readline())
            p = unpack_key_value(f.readline())
        self.public = ElGamalPublicKey(y, g, p)

    def load_private_key(self, private_key_filename: str):
        with open(private_key_filename, 'r') as f:
            x = unpack_key_value(f.readline())
            p = unpack_key_value(f.readline())
        self.private = ElGamalPrivateKey(x, p)

    @classmethod
    def from_file(cls, public_key_filename: str, private_key_filename: str):
        # load public key
        public_key = None
        if public_key_filename is not None:
            with open(public_key_filename, 'r') as f:
                y = unpack_key_value(f.readline())
                g = unpack_key_value(f.readline())
                p = unpack_key_value(f.readline())
            public_key = ElGamalPublicKey(y, g, p)
        # load private key
        private_key = None
        if private_key_filename is not None:
            with open(private_key_filename, 'r') as f:
                x = unpack_key_value(f.readline())
                p = unpack_key_value(f.readline())
            private_key = ElGamalPrivateKey(x, p)
        # return new class instance
        return cls(public_key, private_key)


class ElGamal:
    @staticmethod
    def generate_key_pair():
        p = getPrime(1024)
        g = random.randint(2, p - 1)
        x = random.randint(1, p - 2)
        y = pow(g, x, p)
        return ElGamalKey(ElGamalPublicKey(y, g, p), ElGamalPrivateKey(x, p))

    @staticmethod
    def encrypt(pt, public_key: ElGamalPublicKey):
        # unpack public key
        y, g, p = public_key
        # convert pt to blocks
        pt = plaintext_to_block(pt, len(str(p)) - 1)
        # encrypt
        a = []; b = [];
        for block in pt:
            k = random.randint(1, p - 2)
            a.append(pow(g, k, p))
            b.append((pow(y, k, p) * block) % p)
        # return
        return a, b

    @staticmethod
    def decrypt(ct: tuple, private_key: ElGamalPrivateKey):
        # init
        assert len(ct) == 2
        # unpack private key
        x, p = private_key
        # unpack ciphetext a and b
        ls_a, ls_b = ct
        # decrypt
        pt = []
        for a, b in zip(ls_a, ls_b):
            inv = pow(a, p - 1 - x, p)
            pt.append((b * inv) % p)
        # rebuild pt
        print(pt)
        pt = block_to_plaintext(pt, len(str(p)) - 1)
        # return
        return pt


if __name__ == '__main__':
    key = ElGamal.generate_key_pair()
    # # save
    # key.to_file('test.pub', 'test.pri')
    # # key.to_file('test.pub', None)
    # # load
    # new_key = ElGamalKey.from_file('test.pub', None)
    # # check
    # assert key.public == new_key.public
    # # assert key.private == new_key.private
    # # assert new_key.public is None
    # assert new_key.private is None
    # print('ok')

    # # TEST enc-dec
    # import os
    # for i in range(100):
    #     pt = os.urandom(4)
    #     print(pt)
    #     ct = ElGamal.encrypt(pt, key.public)
    #     print(ct)
    #     new_pt = ElGamal.decrypt(ct, key.private)
    #     assert pt == new_pt
    #     print('ok')

    pt = b'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    print(pt)
    ct = ElGamal.encrypt(pt, key.public)
    print()
    print(ct)
    new_pt = ElGamal.decrypt(ct, key.private)
    print()
    print(new_pt)
    assert pt == new_pt
    print('ok')
