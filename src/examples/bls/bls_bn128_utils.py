from web3 import Web3
from py_ecc import bn128

FQ = bn128.FQ
FQ2 = bn128.FQ2
order = bn128.curve_order
bn128_a = 0xc19139cb84c680a6e14116da060561765e05aa45a1c72a34f082305b61f3f52
bn128_b = 3

def hash_to_ec_g1(msg, ec=bn128, a=bn128_a, b=bn128_b) -> (FQ, FQ):
    if type(msg) is str:
        try:
            msg = int(msg, 16)
            x_bytes = Web3.sha3(msg)
        except ValueError:
            x_bytes = Web3.sha3(text=msg)
    elif (type(msg) is bytes) or (type(msg) is int):
        x_bytes = Web3.sha3(msg)
    else:
        raise ValueError('message not supported by sha3')
    x = Web3.toInt(x_bytes) % ec.curve_order
    while True:
        y_square = addmod((mulmod(mulmod(x, x, ec), x, ec)), b, ec)
        y = expmod(y_square, a, ec)
        if mulmod(y, y, ec) == y_square:
            return FQ(x), FQ(y)
        x = addmod(x, 1, ec)


def mulmod(a: int, b: int, ec=bn128) -> int:
    return (a * b) % ec.field_modulus


def addmod(a: int, b: int, ec=bn128) -> int:
    return (a + b) % ec.field_modulus


def expmod(b: int, e: int, ec=bn128) -> int:
    return pow(b, e, ec.field_modulus)


if __name__ == '__main__':
    print(hash_to_ec_g1('hello, world'))
    print(hash_to_ec_g1(b'\xab\x79\xfb\x80'))
    print(hash_to_ec_g1('ab79fb80'))
    print(hash_to_ec_g1('0xab79fb80'))
    print(hash_to_ec_g1(0xab79fb80))
