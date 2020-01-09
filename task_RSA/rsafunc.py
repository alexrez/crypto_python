import random

def is_prime(number, test_func=None, func_args=None):
    if test_func is None:
        test_func = rabin_miller_test
        func_args = {}
        # return rabin_miller_test(number)
    return test_func(number, **func_args)


def rabin_miller_test(number, log_precision=128):
    # prime: p >= 1 - (1/2) ** (2 * k)
    # True: 1 - (1/2) ** (2 * k) >= 1 - (1/2) ** log_precision => 2 * k >= log_precision


    return 2 * k >= log_precision


def get_next_prime(edge, test_func=None, func_args=None):
    while not is_prime(edge, test_func, func_args):
        edge += 1
    return edge


def gcd(a, b):
    res = [0, 1]
    while b:
        res.append(a // b * res[-1] + res[-2])
        a, b = b, a % b

    d = res[-2]
    if len(res) % 2 != 1:
        d = phi_N - d

    return a, d


def powermod(a, b, mod):
    pass





