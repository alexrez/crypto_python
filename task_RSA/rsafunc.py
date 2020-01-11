import random
import math

def is_prime(number, test_func=None, func_args=None):
    if test_func is None:
        test_func = rabin_miller_test
        func_args = {}
        # return rabin_miller_test(number)
    return test_func(number, **func_args)


def rabin_miller_test(number, log_precision=128):
    # prime: p >= 1 - (1/2) ** (2 * k)
    # True: 1 - (1/2) ** (2 * k) >= 1 - (1/2) ** log_precision => 2 * k >= log_precision
    if number % 2 == 0:
        return False
    k = 0
    s = 0
    t = number - 1
    while t % 2 == 0:
        s += 1
        t >>= 1

    for _ in range(int(math.log(number, 2))):
        a = random.randint(2, number - 2)
        x = powermod(a, t, number)
        if x == 1 or x == number - 1:
            k += 1
            continue
        need_to_return = True
        for s_i in range(s):
            x = x ** 2 % number
            if x == 1:
                return False
            elif x == number - 1:
                k += 1
                need_to_return = False
                break
        if need_to_return:
            return False
    
    return 2 * k >= log_precision


def get_next_prime(edge, test_func=None, func_args=None):
    while not is_prime(edge, test_func, func_args):
        edge += 1
    return edge


def gcd(a, b):
    mod = a
    res = [0, 1]
    while b:
        res.append(a // b * res[-1] + res[-2])
        a, b = b, a % b

    d = res[-2]
    if len(res) % 2 != 1:
        d = mod - d

    return a, d


def powermod(a, b, mod):
    pow_ = int('{0:b}'.format(b)[::-1], 2)
    res = 1
    while pow_:
        res = (res ** 2) * (a ** (pow_ % 2)) % mod
        pow_ >>= 1
    return res

    #recursion may cause stackoverflow
    # if b == 0:
    #     return 1
    # prev_a = powermod(a, b >> 1, mod) ** 2
    # return prev_a * (a ** (b % 2)) % mod

