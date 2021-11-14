import sympy as sp
import random

def generate():
    primes = [p for p in sp.primerange(10**7, 10**8) if p % 4 == 3]

    f = open("primes.txt", "w")
    f.write("\n".join((str(p) for p in primes)))
    f.close()

def bbs_init():
    f = open("primes.txt", "r")
    lines = f.readlines()

    while True:
        p1 = int(random.choice(lines))
        p2 = int(random.choice(lines))

        if p1 != p2 and sp.gcd(p1 * p2, (p1 - 1) * (p2 - 1)) == 1:
            break

    m = p1 * p2
    while True:
        seed = random.randint(2, m)
        if sp.gcd(seed, m) == 1:
            break
    
    return p1, p2, seed