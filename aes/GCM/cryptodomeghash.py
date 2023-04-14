from Crypto.Util._raw_api import (
    load_pycryptodome_raw_lib,
    VoidPointer,
    create_string_buffer,
    get_raw_buffer,
    SmartPointer,
    c_size_t,
    c_uint8_ptr,
)

from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Util import _cpu_features
from Crypto.Util.strxor import strxor
from Crypto.Util.Padding import pad, unpad


# C API by module implementing GHASH
_ghash_api_template = """
    int ghash_%imp%(uint8_t y_out[16],
                    const uint8_t block_data[],
                    size_t len,
                    const uint8_t y_in[16],
                    const void *exp_key);
    int ghash_expand_%imp%(const uint8_t h[16],
                           void **ghash_tables);
    int ghash_destroy_%imp%(void *ghash_tables);
"""


def _build_impl(lib, postfix):
    from collections import namedtuple

    funcs = ("ghash", "ghash_expand", "ghash_destroy")
    GHASH_Imp = namedtuple("_GHash_Imp", funcs)
    try:
        imp_funcs = [getattr(lib, x + "_" + postfix) for x in funcs]
    except AttributeError:  # Make sphinx stop complaining with its mocklib
        imp_funcs = [None] * 3
    params = dict(zip(funcs, imp_funcs))
    return GHASH_Imp(**params)


def _get_ghash_clmul():
    """Return None if CLMUL implementation is not available"""

    if not _cpu_features.have_clmul():
        return None
    try:
        api = _ghash_api_template.replace("%imp%", "clmul")
        lib = load_pycryptodome_raw_lib("Crypto.Hash._ghash_clmul", api)
        result = _build_impl(lib, "clmul")
    except OSError:
        result = None
    return result

gsh_clmul = _get_ghash_clmul()

class _GHASH(object):
    """GHASH function defined in NIST SP 800-38D, Algorithm 2.
    If X_1, X_2, .. X_m are the blocks of input data, the function
    computes:
       X_1*H^{m} + X_2*H^{m-1} + ... + X_m*H
    in the Galois field GF(2^256) using the reducing polynomial
    (x^128 + x^7 + x^2 + x + 1).
    """

    def __init__(self, subkey, ghash_c):
        assert len(subkey) == 16

        self.ghash_c = ghash_c

        self._exp_key = VoidPointer()
        result = ghash_c.ghash_expand(c_uint8_ptr(subkey), self._exp_key.address_of())
        if result:
            raise ValueError("Error %d while expanding the GHASH key" % result)

        self._exp_key = SmartPointer(self._exp_key.get(), ghash_c.ghash_destroy)

        # create_string_buffer always returns a string of zeroes
        self._last_y = create_string_buffer(16)

    def update(self, block_data):
        assert len(block_data) % 16 == 0

        result = self.ghash_c.ghash(
            self._last_y,
            c_uint8_ptr(block_data),
            c_size_t(len(block_data)),
            self._last_y,
            self._exp_key.get(),
        )
        if result:
            raise ValueError("Error %d while updating GHASH" % result)

        return self

    def digest(self):
        return get_raw_buffer(self._last_y)


def ghash_iv(block, H_k):
    ghash_c = gsh_clmul
    fill = (16 - (len(block) % 16)) % 16 + 8
    ghash_in = block + b"\x00" * fill + long_to_bytes(8 * len(block), 8)
    j0 = _GHASH(H_k, ghash_c).update(ghash_in).digest()
    return j0


def ghash(block, H):
    ghash_c = gsh_clmul
    j0 = _GHASH(H, ghash_c).update(block).digest()
    return j0


def get_tag_single_block(iv0, block, zero_key):
    signer = _GHASH(zero_key, gsh_clmul)
    signer.update(block + b'\x00'*(16 - len(block)))
    signer.update(long_to_bytes(len(block) * 8, 16))
    tag = signer.digest()
    tag = strxor(tag, iv0)
    return tag

def get_tag(iv0, A, C, zero_key):
    signer = _GHASH(zero_key, gsh_clmul)

    padlen = (16 - (len(A) % 16)) % 16
    signer.update(A + b'\x00' * padlen)
    padlen = (16 - (len(C) % 16)) % 16
    signer.update(C + b'\x00'*padlen)
 
    signer.update(long_to_bytes(len(A) * 8, 8) + long_to_bytes(len(C) * 8, 8))
    tag = signer.digest()
    tag = strxor(tag, iv0)
    return tag


from Crypto.Util.strxor import strxor

pt, key, iv, enciv, zk, tag_own, tag, additional, ct, authenc = (b'kekkekkekkek', b'\xca\xc3\xf1\xff\x08\xd4\xd7\r\xd0\x8f\xa1%"p\xf4e', b'X\x82+\xd2\xedHZ\x18\xc9\x0b\xca\x02', b'F\x88\xcda@\xb1\xc5Z\x04\x0c\xc4\xcf?q\x83\xd2', b'<\xbf2\t\x9c;p\x0f{0\xebh\xf07\xee]', b'\xf71\x1a\xec\x1cV\xff_\x91\x07\x8d\xbbk\n\x03.', b'\x07\x1d\x04\x9c\x15\x89.\x00V\x1fGs\xd9\xc8\x0ed', b'Crypto', b'!\x80\x08\x13\x9f\xf2"\xb7\x10\xf9\xf3\x89', b'\xe3r\xbb4S.c\xbfH\xe0\xc1\xb3\xf8\xd4a\xf0')

#autenc = ghash(additional + b'\x00' * (16 - len(additional)), zk)

tag1 = get_tag_single_block(enciv, ct, zk)
tag2 = get_tag(enciv, additional, ct, zk)

print(tag2)
print(tag)
print(tag_own)
