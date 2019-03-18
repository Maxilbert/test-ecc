from src.examples.bls.bls_utils import *


def key_gen(priv=9078879759034877109383407430680751358246) -> (int, (FQ2, FQ2)):
    pub = ec.multiply(g2, priv)
    return priv, pub


def sign(msg, priv: int) -> (FQ, FQ):
    digest = hash_to_ec_g1(msg)
    return multiply(digest, priv)


def verify(msg, sig: (FQ, FQ), pub: (FQ2, FQ2)) -> bool:
    digest = hash_to_ec_g1(int.from_bytes(msg.encode(), byteorder='big'))
    lhs = pairing(pub, digest)
    rhs = pairing(g2, sig)
    return lhs == rhs


if __name__ == '__main__':

    # KeyGen() -> (sk, pk)
    sk, pk = key_gen()

    # Sign(msg, sk) -> sig
    sig = sign("hello, world", sk)

    # Verify(msg, sig, pk) -> True/False
    validity = verify("hello, world", sig, pk)

    print(validity)
