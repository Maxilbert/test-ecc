from py_ecc import bn128 as ec
# import sys, resource


def main():
    # resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))
    # sys.setrecurionlimit(10**6)
    g1 = ec.G1
    g2 = ec.G2

    e12 = ec.pairing(g2, g1)
    print(e12)


if __name__ == '__main__':
    main()

