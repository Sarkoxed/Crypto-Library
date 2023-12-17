# https://medium.com/@loveshharchandani/zero-knowledge-proofs-with-sigma-protocols-91e94858a1fb

from sage.all import GF, EllipticCurve, randint
from Crypto.Util.number import getStrongPrime, isPrime, getPrime
from Crypto.Hash import BLAKE2b

def getStrongPrime(n):
    q = 1 + 2 * getPrime(n-1)
    while not isPrime(q):
        q = 1 + 2 * getPrime(n-1)
    return q

def interactive():
    #p = getStrongPrime(512)
    p = 0xeb0164a2bf1cd0a5cbb82787e2d5400a4766f18965f17cd6cafe0506a2d54deb8e26ccefa0e3e8ddfba2dc9bd913ed8d72d64cfc6ec05720ea24a732ddcddd67
    print(p)
    G = GF(p)
    g = G.multiplicative_generator()
    x = randint(1, p - 1)
    y = g**x # goes to verifier
    
    for _ in range(10):
        r = randint(1, p - 1)
        t = g**r # goes to verifier
        
        c = randint(1, p - 1) # goes to prover
        
        s = (r + x * c) % (p - 1) # goes to verifier
        
        assert g**s == y**c * t

def non_interactive():
    #p = getStrongPrime(512)
    p = 0xeb0164a2bf1cd0a5cbb82787e2d5400a4766f18965f17cd6cafe0506a2d54deb8e26ccefa0e3e8ddfba2dc9bd913ed8d72d64cfc6ec05720ea24a732ddcddd67
    print(p)
    G = GF(p)
    g = G.multiplicative_generator()
    x = randint(1, p - 1)
    y = g**x # goes to verifier
    
    for _ in range(10):
        r = randint(1, p - 1)
        t = g**r # goes to verifier
        
        m = b"".join([int(x).to_bytes(512 // 8, 'big') for x in [g, y, t]])
        h = BLAKE2b.new(data=m, digest_bytes=512//8).digest()
        c = int.from_bytes(h, 'big')

        s = (r + x * c) % (p - 1)

        # send (t, s)

        assert g**s == y**c * t

def non_interactive_opt():
    #p = getStrongPrime(512)
    p = 0xeb0164a2bf1cd0a5cbb82787e2d5400a4766f18965f17cd6cafe0506a2d54deb8e26ccefa0e3e8ddfba2dc9bd913ed8d72d64cfc6ec05720ea24a732ddcddd67
    print(p)
    G = GF(p)
    g = G.multiplicative_generator()
    x = randint(1, p - 1)
    y = g**x # goes to verifier
    
    for _ in range(10):
        r = randint(1, p - 1)
        t = g**r # goes to verifier
        
        m = b"".join([int(x).to_bytes(512 // 8, 'big') for x in [g, y, t]])
        h = BLAKE2b.new(data=m, digest_bytes=512//8).digest()
        c = int.from_bytes(h, 'big')
        s = (r + x * c) % (p - 1)

        # sends (c, s)

        t_v = g**s * y**(-c)
        m_v = b"".join([int(x).to_bytes(512 // 8, 'big') for x in [g, y, t_v]])
        h_v = BLAKE2b.new(data=m_v, digest_bytes=512//8).digest()
        c_v = int.from_bytes(h, 'big')
        
        assert c_v == c

def non_interactive_equal_dlogs():
    #p = getStrongPrime(512)
    p = 0xeb0164a2bf1cd0a5cbb82787e2d5400a4766f18965f17cd6cafe0506a2d54deb8e26ccefa0e3e8ddfba2dc9bd913ed8d72d64cfc6ec05720ea24a732ddcddd67
    print(p)
    G = GF(p)
    g = G.multiplicative_generator()
    h = G.random_element()
    x = randint(1, p - 1)

    y = g**x # goes to verifier
    z = h**x # goes to verifier

    for _ in range(10):
        r = randint(1, p - 1)
        t1 = g**r # goes to verifier
        t2 = h**r
                
        m = b"".join([int(x).to_bytes(512 // 8, 'big') for x in [g, h, y, z, t1, t2]])
        ha = BLAKE2b.new(data=m, digest_bytes=512//8).digest()
        c = int.from_bytes(ha, 'big')
        s = (r + x * c) % (p - 1)
        
        # sends (t1, t2, s)

        assert g**s == y**c * t1 and h**s == z**c * t2

def batch_and():
    #p = getStrongPrime(512)
    p = 0xeb0164a2bf1cd0a5cbb82787e2d5400a4766f18965f17cd6cafe0506a2d54deb8e26ccefa0e3e8ddfba2dc9bd913ed8d72d64cfc6ec05720ea24a732ddcddd67
    print(p)
    G = GF(p)
    g = G.multiplicative_generator()
    h = G.random_element()
    a = randint(1, p - 1)
    y = g**a # goes to verifier

    b = randint(1, p - 1)
    z = h**b # goes to verifier

    for _ in range(10):
        r1 = randint(1, p - 1)
        t1 = g**r1 # goes to verifier

        r2 = randint(1, p - 1)
        t2 = h**r2

        m = b"".join([int(x).to_bytes(512 // 8, 'big') for x in [g, h, y, z, t1, t2]])
        ha = BLAKE2b.new(data=m, digest_bytes=512//8).digest()
        c = int.from_bytes(ha, 'big')
        s1 = (r1 + a * c) % (p - 1)
        s2 = (r2 + b * c) % (p - 1)
        
        # sends (t1, t2, s)

        assert g**s1 == y**c * t1 and h**s2 == z**c * t2

def batch_or():
    #p = getStrongPrime(512)
    p = 0xeb0164a2bf1cd0a5cbb82787e2d5400a4766f18965f17cd6cafe0506a2d54deb8e26ccefa0e3e8ddfba2dc9bd913ed8d72d64cfc6ec05720ea24a732ddcddd67
    print(p)
    G = GF(p)
    g = G.multiplicative_generator()
    h = G.random_element()
    a = randint(1, p - 1)
    y = g**a

    b = randint(1, p - 1)
    z = h**b 

    for _ in range(10): # sps prover knows a
        r1 = randint(1, p - 1)
        t1 = g**r1 # goes to verifier

        c2 = randint(1, p - 1)
        s2 = randint(1, p - 1)
        t2 = h**s2 * z**(-c2)

        m = b"".join([int(x).to_bytes(512 // 8, 'big') for x in [g, h, y, z, t1, t2]])
        ha = BLAKE2b.new(data=m, digest_bytes=512//8).digest()
        c = int.from_bytes(ha, 'big')
        c1 = (c - c2) % (p - 1)
        
        s1 = (r1 + a * c1) % (p - 1)
        
        # sends (t1, c1, s1), (t2, c2, s2)

        assert g**s1 == y**c1 * t1 and h**s2 == z**c2 * t2



#interactive()
batch_or()
