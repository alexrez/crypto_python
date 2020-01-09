import os
import json
import random
import math

import rsafunc


class RSAKey:

    def __init__(self, power=None, mod=None):
        if power is not None and mod is not None:
            if (power <= 0) or (mod <= 0):
                raise ValueError("allows '0 < power' and '0 < mod'")
            else:
                power %= mod
        self.__power = power
        self.__mod = mod


    @property
    def power(self):
        return self.__power


    @power.setter
    def power(self, new_power):
        self.__power = new_power % mod


    @property
    def mod(self):
        return self.__mod


    @mod.setter
    def mod(self, new_mod):
        self.__mod = new_mod
        self.__power %= new_mod


    def __repr__(self):
        params = []
        for param in self.__dict__.items():
            value = str(param[1])
            if len(value) > 8:
                value = value[:8] + '<..' + str(len(value) - 8) + '..>'
            params.append('='.join([param[0], value]))

        return self.__class__.__name__ + '(' + ', '.join(params) + ')'


    def __str__(self):
        return json.dumps(', '.join(['='.join([param[0], str(param[1])])for param in self.__dict__.items()]))
        # return self.__class__.__name__ + '(' + ', '.join(['='.join([param[0], str(param[1])])for param in self.__dict__.items()]) + ')'


    def dump(self, file_name=None):
        if file_name is None:
            # file_name = [v for k, v in self.__dict__.items() if '__file_name' in k][0]
            if self.__class__.__name__ == 'RSAPubKey':
                file_name = 'rsa.pub'
            elif self.__class__.__name__ == 'RSASecKey':
                file_name = 'rsa.key'
            else:
                raise ValueError("file_name is required")
        file_path = os.path.normpath(os.path.expanduser(file_name))
        with open(file_path, 'w') as file:
            file.write(self.__str__())


    def load(self, file_name=None):
        if file_name is None:
            # file_name = [v for k, v in self.__dict__.items() if '__file_name' in k][0]
            if self.__class__.__name__ == 'RSAPubKey':
                file_name = 'rsa.pub'
            elif self.__class__.__name__ == 'RSASecKey':
                file_name = 'rsa.key'
            else:
                raise ValueError("file_name is required")
        file_path = os.path.normpath(os.path.expanduser(file_name))
        with open(file_path, 'r') as file:
            list(map(lambda attr: setattr(self, attr[0], int(attr[1])), [attr.split('=') for attr in json.loads(file.read()).split(', ')]))


class RSAPubKey(RSAKey):

    def __init__(self, *args):
        super(RSAPubKey, self).__init__(*args)
        # self.__file_name = 'rsa.pub'


class RSASecKey(RSAKey):

    def __init__(self, *args):
        super(RSASecKey, self).__init__(*args)
        # self.__file_name = 'rsa.key'


class RSACrypto():

    def __init__(self, pub_key, sec_key):
        if pub_key.mod != sec_key.mod:
            raise ValueError("pub_key.mod != sec_key.mod")
        self.__N = pub_key.mod
        self.__pub_key = pub_key
        self.__sec_key = sec_key


    @property
    def block_len(self):
        return int(math.log(self.__N, 2))


    def encrypt(self, block):
        return rsafunc.powermod(block, self.__pub_key.power, self.__N)


    def decrypt(self, block):
        return rsafunc.powermod(block, self.__sec_key.power, self.__N)


    def encrypts(self, message):
        return self.encryptb([ord(sym) for sym in message])
    

    def decrypts(self, cyphertext):
        return ''.join([chr(b) for b in self.decryptb(cyphertext)])
        

    def encryptb(self, message):
        concat_mes = ''.join(['{0:>0{width}b}'.format(t, width=8) for t in message])
        block_len_ = self.block_len
        split_mes = [concat_mes[i: i + block_len_] for i in range(0, len(concat_mes), block_len_)]
        return ''.join(['{0:>0{width}x}'.format(block, width=block_len_) for block in [self.encrypt(int(m, 2)) for m in split_mes]])


    def decryptb(self, cyphertext):
        block_len_ = self.block_len
        blocked_text = [self.decrypt(int(cyphertext[i: i + block_len_], 16)) for i in range(0, len(cyphertext), block_len_)]
        concat_mes = ''.join(['{0:>0{width}b}'.format(block, width=block_len_) for block in blocked_text])
        return [int(concat_mes[i: i + 8], 2) for i in range(0, len(concat_mes), 8)]


def gen_keys(number, half_len=256):
    # half_len- битовая длина простых чисел p и q
    left_border = (1 << (half_len - 1)) + 1
    right_border = (1 << half_len) - 1
    p = rsafunc.get_next_prime(random.randint(left_border, right_border))
    while p > right_border:
        p = rsafunc.get_next_prime(random.randint(left_border, right_border))
    q = rsafunc.get_next_prime(random.randint(left_border, right_border))
    while p == q or q > right_border:
        q = rsafunc.get_next_prime(random.randint(left_border, right_border))

    N = p * q
    phi_N = (p - 1) * (q - 1)
    e = random.randint(2, phi_N - 1)
    gcd_, d = rsafunc.gcd(phi_N, e)
    while gcd_ != 1:
        e = random.randint(2, phi_N - 1)
        gcd_, d = rsafunc.gcd(phi_N, e)
    # print(e, d, N)
    return RSACrypto(RSAPubKey(e, N), RSASecKey(d, N))


# rsa = gen_keys(1234567, 4)
# print(rsa.block_len)
# encr = rsa.encrypt(3) 
# print(encr)

# print(rsa.decrypt(encr))









