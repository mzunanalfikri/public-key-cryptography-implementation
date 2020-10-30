from sympy import randprime
import random


class RSA:
    def __init__(self, key_size=10):
        self.key_size = key_size
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

    def encrypt(self, plaintext):
        # TODO : load ke block
        x = pow(plaintext, self.e, self.n)
        print(x)
        return x
    
    def decrypt(self, ciphertext):
        # TODO : load ke block
        x = pow(ciphertext, self.d, self.n)
        print(x)
        return x

if __name__ == "__main__":
    rsa = RSA()
    temp = rsa.encrypt(999)
    rsa.decrypt(temp)

