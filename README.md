## My own crypto library contents

### RSA 
- Full/Partial(brutable) knowledge of d
    - python + cpp implementation
- PKCS1 padding oracle attack
    - python + cpp implementation
- Notes on RSA key creation using python/openssl
- Wiener attack on RSA with small private exponent
- Known bits of p

### DLP
- Collision Algos
    - Baby-Step-Giant-Step implementation in python
    - Birthday Paradox based collision algorithm implementation in python
- Pollard Rho
    - Pollard Rho algorithm implementation in python(Including Field extensions)

### Elliptic Curve Cryptography
- ECC implementation in python
- Weil Pairing implementation in python
- ECDH implementation in python
- ecdsa
    - Elliptic Curve DSA implementation in python
- Anomalous Curves
    - Smart attack implementation in python
- MOV
    - MOV algorithm implementation in python
    - MOV algorithm(not mine)

### Lattice Cryptography 
- LLL
    - LLL algorithm implementation in python
    - Improved spped LLL algorithm
    - LLL sage? why
- cpp tools to analyze lattices
    - lattice attacks
        - LLL
        - HadamardRatio
        - Gram-Schmidt
        - LLL_check reduced basis
        - Babai Closest Plain
        - Babai Closest Vertex
        - Gaussian Expected Length
            
- Congruential Public Key CS
- GGH Public Key CS
    - ggh implementation in python
    - gghdsa implementation in python
- KnapSack like CS
    - subset sum 
    - superincreasing knapsack
- NTRU Public Key CS
    - NTRU implemntation in python
    - NTRUMLS implementation in python

### Integer Relation
- Algebraic Roots recovery using LLL(square and cubic)
- Coppersmith attacks
- Finding an Algebraic relation using sage

### AES
- CBC Mode
    - Padding Oracle attack implementation
- GCM
    - Ghash implementation(not mine)
- Ordinary AES implementation in python
- Sbox gen implementation in c
- Example of Linear sbox usage in aes

### RC4
- oracle implemenation in python
- RC4 cipher implementation in python
- 1st Round Attack on RC4
    - 1st round attack on rc4 IV||main_key
    - 1st round attack on rc4 main_key||IV
    - Chosen IV attack on rc4
- 2nd Round Attack on RC4
    - 2nd round attack on rc4 IV||main_key
- FMS attack on RC4
- Special IV generation


### Permutation Ciphers
- Rail Fence cipher

### Simple substitution
- Shift cipher + analysis
- Vigenere Cipher + analysis
- frequencies
    - bigrams
    - singles

### HASH Functions
- sha1 implementation

### Based
- Bacon cipher

### TOOLS
- Factorization methods
    - EC factorization
    - Fermatt Factorization
    - Naive Factorization
    - Pollard P Factorization
    - Pollard Rho Factorization
    - Stackoverflow
- Inverse modulo
- Primeness check + gen
    - is prime
    - Atkin
    - Simple Prime in range finder
    - Euler's pattern to find primes
    - Brute
    - Sundaram
- Binary Search
- Smooth Primes Creation
- Interval Union
- Legandre symbol
- use of gmp example
- use of z3 example
- use of cado-nfs example
