from src.examples.bls.bls_bn128_utils import *
from py_ecc import bn128


def key_gen(privkey=9078879759034877109383407430680751358246, ec=bn128) -> (int, (FQ2, FQ2)):
    pubkey = ec.multiply(ec.G2, privkey)
    return privkey, pubkey


def sign(message, privkey: int, ec=bn128) -> (FQ, FQ):
    digest = hash_to_ec_g1(message)
    return ec.multiply(digest, privkey)


def verify(message, signature: (FQ, FQ), pubkey: (FQ2, FQ2), ec=bn128) -> bool:
    digest = hash_to_ec_g1(message)
    lhs = ec.pairing(pubkey, digest)
    rhs = ec.pairing(ec.G2, signature)
    return lhs == rhs


if __name__ == '__main__':

    # KeyGen() -> (sk, pk)
    sk, pk = key_gen()

    # Sign(msg, sk) -> sig
    sig = sign("hello, world", sk)

    # Verify(msg, sig, pk) -> True/False
    validity = verify("hello, world", sig, pk)

    print(validity)
