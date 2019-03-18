from web3 import Web3
from py_ecc import bn128 as ec

FQ = ec.FQ
FQ2 = ec.FQ2
g1 = ec.G1
g2 = ec.G2
order = ec.curve_order
pairing = ec.pairing
is_on_curve = ec.is_on_curve
multiply = ec.multiply

a = FQ(0xc19139cb84c680a6e14116da060561765e05aa45a1c72a34f082305b61f3f52)


def hash_to_ec_g1(msg) -> (FQ, FQ):
    if type(msg) is str:
        try:
            msg = int(msg, 16)
            x_bytes = Web3.sha3(msg)
        except ValueError:
            x_bytes = Web3.sha3(text=msg)
    elif type(msg) is (int or bytes):
        x_bytes = Web3.sha3(msg)
    else:
        raise ValueError('message not supported by sha3')
    x = Web3.toInt(x_bytes) % order
    while True:
        y_square = addmod((mulmod(mulmod(x, x), x)), 3)
        y = expmod(y_square, a.n)
        if mulmod(y, y) == y_square:
            return FQ(x), FQ(y)
        x = addmod(x, 1)


def mulmod(a: int, b: int, field_modulus=ec.field_modulus) -> int:
    return (a * b) % field_modulus


def addmod(a: int, b: int, field_modulus=ec.field_modulus) -> int:
    return (a + b) % field_modulus


def expmod(b: int, e: int, field_modulus=ec.field_modulus) -> int:
    return pow(b, e, field_modulus)
