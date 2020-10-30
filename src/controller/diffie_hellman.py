class DiffieHellman:
    def __init__(self, n, g, x, y):
        self.n = n
        self.g = g
        self.x = x
        self.y = y
        # calculate shared key
        self.X = pow(self.g, self.x, self.n)
        self.Y = pow(self.g, self.y, self.n)
        self.K = pow(pow(g, x, n), y, n)
        assert pow(self.X, self.y, self.n) == pow(self.Y, self.x, self.n) == self.K

    def get_shared_key(self):
        return self.K

    def simulate_key_exchange(self):
        # Alice and Bob agreed n and g publicly
        print(f'Alice and Bob agreed n = {self.n} and g = {self.g}')
        yield self.n, self.g
        # Alice choose x privately, then calculate and send X to Bob
        print('Step 1')
        print(f'Alice chooses x = {self.x}')
        print(f'Alice sends X = (g^x) mod n = {self.X} to Bob')
        yield self.x, self.X
        # Bob choose y privately, then calculate and send Y to Alice
        print('Step 2')
        print(f'Bob chooses y = {self.y}')
        print(f'Bob sends Y = (g^y) mod n = {self.Y} to Alice')
        yield self.y, self.Y
        # Alice calculate simetric key K
        print('Step 3')
        print(f'Alice calculates K = (Y^x) mod n = {self.K}')
        yield self.K
        # Bob calculate simetric key K
        print('Step 4')
        print(f'Bob calculates K = (X^y) mod n = {self.K}')
        yield self.K
        # Last
        print(f'Alice and Bob has same simetric key K = {self.K}')
        yield self.K


if __name__ == '__main__':
    d = DiffieHellman(97, 5, 36, 58)
    g = d.simulate_key_exchange()
    val = next(g, None)
    while val is not None:
        val = next(g, None)
