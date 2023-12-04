from string import ascii_lowercase, ascii_uppercase, punctuation, digits
from math import floor
import json
from random import choices

def shift_text(pt, delta, alphabet):
    ct = []
    for c in pt:
        j = alphabet.index(c)
        new_index = (j + delta) % len(alphabet)
        ct.append(alphabet[new_index])
    return bytes(ct)

def encrypt(pt, key, alphabet):
    N = len(alphabet)
    K = len(key)
    
    ct = []
    j = 0
    for c in pt:
        if c in alphabet:
            i = alphabet.index(c)
            k = alphabet.index(key[j % K])
            newc = alphabet[(i + k) % N]
            j += 1
        else:
            newc = c
        ct.append(newc)
    return bytes(ct)

def decrypt(ct, key, alphabet):
    N = len(alphabet)
    K = len(key)
    
    pt = []
    j = 0
    for c in ct:
        if c in alphabet:
            i = alphabet.index(c)
            k = alphabet.index(key[j % K])
            newc = alphabet[(i - k) % N]
            j += 1
        else:
            newc = c
        pt.append(newc)
    return bytes(pt)

def indco(text, alphabet):
    n = len(text)
    freqs = [text.count(x) for x in alphabet]
    return sum(f * (f - 1) for f in freqs) / (n * (n - 1))

def indco_natural(n = 10000):
    alphabet = ascii_lowercase
    probs = json.load(open("frequencies/one.json"))
    freqs = [floor(float(probs[x]) * n) for x in alphabet]
    return sum(f * (f - 1) for f in freqs) / (n * (n - 1))

def try_k(text, k, natindco, randindco, alphabet, stat, coeff=0.75):
    differences_rand = []
    differences_nat = []

    for i in range(k):
        tmp = text[i::k]
        ic = indco(tmp, alphabet)
        differences_nat.append(ic - natindco)
        differences_rand.append(ic - randindco)
    
    # sum of squares
    rand_diff = stat(differences_rand)
    nat_diff = stat(differences_nat)

    return nat_diff < rand_diff and nat_diff / rand_diff < coeff, nat_diff, rand_diff # TODO: provide more delicate hypothesis check

def find_k(ct, stat, alphabet, natind=indco_natural):
    natindco = natind()
    randindco = 1 / len(alphabet)
    k_range = len(ct) // 10 # so we won't analyze any substrings of length like 5 or smth
    
    possible_ks = []
    for k in range(1, k_range):
        res, _, _ = try_k(ct, k, natindco, randindco, alphabet, stat)
        if res:
            possible_ks.append(k)
    return possible_ks

def mutual_indco(s, t, alphabet):
    n = len(s)
    m = len(t)
    
    return sum(s.count(x) * t.count(x) for x in alphabet) / (n * m)

def find_possible_keys(ct, possible_lens, alphabet):
    possible_keys = {k: [] for k in possible_lens}
    for k in possible_lens:
        possible_shifts = []
        parts = [bytes(ct[i::k]) for i in range(k)]
        s0 = parts[0]

        for s in parts[1:]:
            max_ind = 0
            shift = -1
            for sigma in range(len(alphabet)):
                shifted_s = shift_text(s, sigma, alphabet)
                mutindco = mutual_indco(s0, shifted_s, alphabet)
                if mutindco > max_ind:
                    max_ind = mutindco
                    shift = sigma

            possible_shifts.append(shift)

        for initial_shift in range(len(alphabet)):
            key_rec = bytes([alphabet[initial_shift]] + [alphabet[(initial_shift - pos_shift) % N] for pos_shift in possible_shifts])
            possible_keys[k].append(key_rec)

    return possible_keys

if __name__ == "__main__":
    with open("frequencies/some_text", "rt") as f:
        text = f.read().lower().encode() * 5

    alphabet = ascii_lowercase.encode()
    N = len(alphabet)

    n = 101
    key = bytes(choices(alphabet, k=n))
    ct = encrypt(text, key, alphabet)
    sanitized_ct = bytes(x for x in ct if x in alphabet) # don't include punctuation and digits
    
#    stat = lambda x: sum(a**2 for a in x) # square difference
#    print(find_k(ct, stat))
    stat = lambda x: sum([abs(a) for a in x]) / len(x) if len(x) > 0 else 0# avg - seems to be better
    possible_lens = find_k(sanitized_ct, stat, alphabet)
    print(possible_lens)

    possible_keys = find_possible_keys(sanitized_ct, possible_lens, alphabet)
    print(key in possible_keys[len(key)])
