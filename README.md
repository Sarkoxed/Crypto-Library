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
- Auxialry Inputs
    - attack todo

### Elliptic Curve Cryptography
- ECC implementation in python
- Weil Pairing implementation in python
- ECDH implementation in python
- ecdsa
    - Elliptic Curve DSA implementation in python
    - attacks.py:
        - Linear Congruece attack
        - Polynomial Congruence attack
        - Repeated Nonce attack
        - Lattice Based attack(lower bits)
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

### Algebraic Things
- Ring structure of polynomial quotient ring
    - Order of a multplicative subgroup
    - All the possible orders in this group
    - Ring factorization
    - TODO: find the number of elements in the group s.t. their order is K | minimal_power
- matrices
    - Get jordan General Decomposition of a matrix over a finite field
    - Find the matrix order with help of previous thing
    - lfsr analysis with help of matrix order

### AES
- CBC Mode
    - Padding Oracle attack implementation
- GCM
    - Ghash implementation in python
    - pycryptodome ghash implementation
- Ordinary AES implementation in python
- Sbox gen implementation in c
- Example of Linear sbox usage in aes
- other_implementations
    - open source implementations of aes

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

### Linear Cryptoanalisys
- TODO


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

### ZKP
- KZG
    - KSG implementation from RealWorldCTF2023
- coolstuff
    - Emulated Field operations
- PLONK
    - plonk todo
- sumcheck
    - sumcheck protocol implementation TODO improve....
- protostar/

### Polynomials
- Grobner basis implentation

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
- Carmichael Numbers
    - Generating Carmichael Numbers
    - Testing for Charmichaelness
- Strong PseudoPrimes
    - Generating Strong Pseudoprimes using Arnault algorithm!!!
- Other - some thoughts, theories and algorithms of my own implementation
    - Combinatorics
    - Math
- cvc5
    - cvc5 ff use case
    - ecc solver(lol)
- Binary Search
- Smooth Primes Creation
- Finding roots of a polynomial modulo prime power
- Solving DLP modulo prime power
- Interval Union
- Legendre symbol
- Base n function
- use of gmp example
- use of z3 example
- use of cado-nfs example
- x509cert_help.py - cert generation in python
