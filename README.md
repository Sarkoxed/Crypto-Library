## My crypto library contents

### AES
- CBC Mode
    - Padding Oracle attack implementation
- GCM
    - Ghash implementation in python
    - oracle_access.py - GHASH without knowledge of key

- linear_analysis
    - Example of Linear sbox usage in aes
    - 

- other_implementations
    - open source implementations of aes

- Ordinary AES implementation in python
- Sbox gen implementation in c

### Based
- Bacon cipher


### Block Ciphers
- 

### DLP
- Collision Algos
    - Baby-Step-Giant-Step implementation in python
    - Birthday Paradox based collision algorithm implementation in python
- Pollard Rho
    - Pollard Rho algorithm implementation in python(Including Field extensions)
- Auxialry Inputs
    - attack todo
- prime_power
    - Discrete log in the rings $\frac{ZZ}{p^sZZ}$ up to the power $p^{s-1}, s \ge 2$
    - dlp_modulo_prime_power.py - todo
- Pohlig-Hellman
    - based

### Elliptic Curve Cryptography
- curves
    - elliptic_curves.py  - python implementation of an arbitrary elliptic curve
        - including constant time multiplication
    - edwards_curve.py    - python implmentation of Edwards curves
    - montgomery_curve.py - python implementation of Montgomery curves
    - equivalence.py      - translation between curves
    - kind.sage           - script that kinda automates curve analysis
    - kinds.md            - Writeup on Elliptic Curve kinds
    - get_curves_of_specific_order.py - just elliptic curves order properties
- order
    - curve_order.py - computation of elliptic curve order over finite field using bsgs

    - division_polynomial.py - computation of division_polynomials and rational functions for elliptic curves
        - including computation with unknown y
    - schoofs_algorithm.py - Schoof's algorithm to compute elliptic curve order over finite field
    - multiplication - implmentations of several techniques to boost multiplication

- ecdsa
    - ecdsa.py  - Elliptic Curve DSA implementation in python
    - attacks.py:
        - Linear Congruece attack
        - Polynomial Congruence attack
        - Repeated Nonce attack
        - Lattice Based attack(lower bits)

- Anomalous Curves
    - Smart attack
    - Smart attack but mod p^2
    - Augmented addition attack
    - Fast multiplication using anomalous curves

- MOV
    - weil_pairing.py - weil pairing python implementation
    - MOV algorithm implementation in python using weil pairing
- Supersingular Curves
    - Supersingularity tests
    - Fast multiplication using supersingular curves
- Singular Curves
    - DLP on singular curves

### HASH Functions
- sha1
    - sha1 implentation in python(stolen)
    - length_extension.py - le attack on sha1

- murmurhash3
    - murmurhash3_128.py
    - murmurhash3_128_x64.cpp

    - reverse_murmurhash.py - zero finder/collision finder
- md5
    - md5.py
    - diff.py - d

### Lattice Cryptography 
- LLL
    - LLL algorithm implementation in python
    - Improved spped LLL algorithm
    - LLL sage? why

- cpp_lattice - tools to analyze lattices
    - lattice_attacks.cpp
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

- Integer Relation
    - Algebraic Roots recovery using LLL(square and cubic)
    - Coppersmith attacks
    - Finding an Algebraic relation using sage
- LWE
    - not so much yet

### Linear Cryptoanalisys
- TODO

### Permutation Ciphers
- Rail Fence cipher
- Symmetric_Group
    - Sqrt in S(n)

### PRNG 
- xorshift128p - truncated xorshift128p analysis
    - TODO

### RSA 
- Full/Partial(brutable) knowledge of d
    - python + cpp implementation

- PKCS1 padding oracle attack
    - python + cpp implementation

- Notes on RSA key creation using python/openssl - todo
- wiener - Wiener attack on RSA with small private exponent
    - wiener.py
- Known bits of p

### Simple substitution
- Shift cipher + analysis
- Vigenere Cipher + analysis
- frequencies
    - bigrams
    - singles

### Stream Ciphers

- RC4
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

- LFSR
    - lfsr decomposition

### ZKP
- KZG
    - KZG implementation from RealWorldCTF2023
- coolstuff
    - emulated_field.py   - prove a * b = c(mod q)
    - discrete_log.py     - prove bunch of facts about dl)
    - range_constraint.py - prove that a is less than 2^n
- PLONK
    - plonk todo
- sumcheck
    - sumcheck protocol implementation TODO improve....
- protostar/

### TOOLS

- Algebraic Things
    - polynomials_mod_prime_power.py -  Finding roots of a polynomial modulo prime power
    - polynomial_ring_analysis.py - Ring structure of polynomial quotient ring
        - Order of a multplicative subgroup
        - All the possible orders in this group
        - Ring factorization
        - TODO: find the number of elements in the group s.t. their order is K | minimal_power
    - matrices
        - Get jordan General Decomposition of a matrix over a finite field
        - Find the matrix order with help of previous thing
        - lfsr analysis with help of matrix order
    - Polynomials
        - Groebner basis implentation
        - symmetric_polynomials
            - symmetric_polynomial_decomposition.py - decompose any multivariate symmetric polynomial using symmetric_polynomial basis.


- Factorization methods
    - 4p1factorization
        - Cheng's method - TODO
        - Simplified Cheng's method

    - EC(Lenstra) factorization
    - Fermatt Factorization
    - Naive Factorization
    - Pollard P Factorization
    - Pollard Rho Factorization
    - Stackoverflow
- Inverse modulo
- Primeness check + gen
    - is_prime
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
- cvc5
    - cvc5 ff use case
    - ecc solver(lol)
- Other - some thoughts, theories and algorithms of my own implementation
    - Combinatorics
    - Math

- binary_search.py        - Binary Search
- create_smooth_prime.py  - Smooth Primes Creation
- Interval Union          - 
- Legendre symbol         - 
- rebase.py               - Base n function
- use of gmp example
- use of z3 example
- use of cado-nfs example
- use of pari library
- x509cert_help.py - cert generation in python
