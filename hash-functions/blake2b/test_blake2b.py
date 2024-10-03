import pytest
from os import urandom
from random import randint

from blake2b import Blake2b
from hashlib import blake2b

import struct


def get_msg(n):
    for _ in range(n):
        yield [urandom(randint(1, 1000)).hex(), randint(1, 64)]


@pytest.mark.parametrize("m, n", get_msg(1000))
def test_blake2b(m, n):
    m = bytes.fromhex(m)
    h1 = Blake2b(digest_size=n)
    h1.update(m, True)
    d1 = h1.digest()
    d2 = blake2b(m, digest_size=n).digest()
    assert d1 == d2


# Test vectors
# Unkeyed hash of abc


def test_iv_generation():
    bk = Blake2b()

    iv = [
        0x6A09E667F3BCC908,
        0xBB67AE8584CAA73B,
        0x3C6EF372FE94F82B,
        0xA54FF53A5F1D36F1,
        0x510E527FADE682D1,
        0x9B05688C2B3E6C1F,
        0x1F83D9ABFB41BD6B,
        0x5BE0CD19137E2179,
    ]
    assert bk.iv == iv


def test_conv_and_padding():
    data = b"abc"
    padlen = -len(data) % 128
    data += b"\x00" * padlen
    block = struct.unpack("<16Q", data)

    assert list(block) == [0x636261] + [0] * 15


def test_compression_pre_round_0():
    hsh = Blake2b()
    t = 3

    v = hsh.h.copy() + hsh.iv.copy()
    v[12] ^= t % 2**hsh.w
    v[13] ^= t >> hsh.w
    v[14] ^= 2**hsh.w - 1

    res = [
        0x6A09E667F2BDC948,
        0xBB67AE8584CAA73B,
        0x3C6EF372FE94F82B,
        0xA54FF53A5F1D36F1,
        0x510E527FADE682D1,
        0x9B05688C2B3E6C1F,
        0x1F83D9ABFB41BD6B,
        0x5BE0CD19137E2179,
        0x6A09E667F3BCC908,
        0xBB67AE8584CAA73B,
        0x3C6EF372FE94F82B,
        0xA54FF53A5F1D36F1,
        0x510E527FADE682D2,
        0x9B05688C2B3E6C1F,
        0xE07C265404BE4294,
        0x5BE0CD19137E2179,
    ]

    assert v == res


def test_compression_round_0():
    hsh = Blake2b()
    t = 3

    v = hsh.h.copy() + hsh.iv.copy()
    v[12] ^= t % 2**hsh.w
    v[13] ^= t >> hsh.w
    v[14] ^= 2**hsh.w - 1

    data = b"abc"
    padlen = -len(data) % 128
    data += b"\x00" * padlen

    block = struct.unpack("<16Q", data)

    hsh = Blake2b()
    v = hsh.h.copy() + hsh.iv.copy()
    v[12] ^= t % 2**hsh.w
    v[13] ^= t >> hsh.w
    v[14] ^= 2**hsh.w - 1

    s = hsh.sigma[0]

    v = hsh.Gmix(v, 0, 4, 8, 12, block[s[0]], block[s[1]])
    v = hsh.Gmix(v, 1, 5, 9, 13, block[s[2]], block[s[3]])
    v = hsh.Gmix(v, 2, 6, 10, 14, block[s[4]], block[s[5]])
    v = hsh.Gmix(v, 3, 7, 11, 15, block[s[6]], block[s[7]])

    v = hsh.Gmix(v, 0, 5, 10, 15, block[s[8]], block[s[9]])
    v = hsh.Gmix(v, 1, 6, 11, 12, block[s[10]], block[s[11]])
    v = hsh.Gmix(v, 2, 7, 8, 13, block[s[12]], block[s[13]])
    v = hsh.Gmix(v, 3, 4, 9, 14, block[s[14]], block[s[15]])

    res = [
        0x86B7C1568029BB79,
        0xC12CBCC809FF59F3,
        0xC6A5214CC0EACA8E,
        0x0C87CD524C14CC5D,
        0x44EE6039BD86A9F7,
        0xA447C850AA694A7E,
        0xDE080F1BB1C0F84B,
        0x595CB8A9A1ACA66C,
        0xBEC3AE837EAC4887,
        0x6267FC79DF9D6AD1,
        0xFA87B01273FA6DBE,
        0x521A715C63E08D8A,
        0xE02D0975B8D37A83,
        0x1C7B754F08B7D193,
        0x8F885A76B6E578FE,
        0x2318A24E2140FC64,
    ]
    assert v == res


def test_compression_round_1():
    data = b"abc"
    padlen = -len(data) % 128
    data += b"\x00" * padlen

    block = struct.unpack("<16Q", data)

    hsh = Blake2b()

    v = [
        0x86B7C1568029BB79,
        0xC12CBCC809FF59F3,
        0xC6A5214CC0EACA8E,
        0x0C87CD524C14CC5D,
        0x44EE6039BD86A9F7,
        0xA447C850AA694A7E,
        0xDE080F1BB1C0F84B,
        0x595CB8A9A1ACA66C,
        0xBEC3AE837EAC4887,
        0x6267FC79DF9D6AD1,
        0xFA87B01273FA6DBE,
        0x521A715C63E08D8A,
        0xE02D0975B8D37A83,
        0x1C7B754F08B7D193,
        0x8F885A76B6E578FE,
        0x2318A24E2140FC64,
    ]

    s = hsh.sigma[1]

    v = hsh.Gmix(v, 0, 4, 8, 12, block[s[0]], block[s[1]])
    v = hsh.Gmix(v, 1, 5, 9, 13, block[s[2]], block[s[3]])
    v = hsh.Gmix(v, 2, 6, 10, 14, block[s[4]], block[s[5]])
    v = hsh.Gmix(v, 3, 7, 11, 15, block[s[6]], block[s[7]])

    v = hsh.Gmix(v, 0, 5, 10, 15, block[s[8]], block[s[9]])
    v = hsh.Gmix(v, 1, 6, 11, 12, block[s[10]], block[s[11]])
    v = hsh.Gmix(v, 2, 7, 8, 13, block[s[12]], block[s[13]])
    v = hsh.Gmix(v, 3, 4, 9, 14, block[s[14]], block[s[15]])

    res = [
        0x53281E83806010F2,
        0x3594B403F81B4393,
        0x8CD63C7462DE0DFF,
        0x85F693F3DA53F974,
        0xBAABDBB2F386D9AE,
        0xCA5425AEC65A10A8,
        0xC6A22E2FF0F7AA48,
        0xC6A56A51CB89C595,
        0x224E6A3369224F96,
        0x500E125E58A92923,
        0xE9E4AD0D0E1A0D48,
        0x85DF9DC143C59A74,
        0x92A3AAAA6D952B7F,
        0xC5FDF71090FAE853,
        0x2A8A40F15A462DD0,
        0x572D17EFFDD37358,
    ]
    assert v == res


def test_finalize():
    hsh = Blake2b()

    v = [
        0x12EF8A641EC4F6D6,
        0xBCED5DE977C9FAF5,
        0x733CA476C5148639,
        0x97DF596B0610F6FC,
        0xF42C16519AD5AFA7,
        0xAA5AC1888E10467E,
        0x217D930AA51787F3,
        0x906A6FF19E573942,
        0x75AB709BD3DCBF24,
        0xEE7CE1F345947AA4,
        0xF8960D6C2FAF5F5E,
        0xE332538A36B6D246,
        0x885BEF040EF6AA0B,
        0xA4939A417BFB78A3,
        0x646CBB7AF6DCE980,
        0xE813A23C60AF3B82,
    ]

    h = hsh.h.copy()
    for i in range(8):
        h[i] ^= v[i] ^ v[i + 8]

    res = [
        0x0D4D1C983FA580BA,
        0xE9F6129FB697276A,
        0xB7C45A68142F214C,
        0xD1A2FFDB6FBB124B,
        0x2D79AB2A39C5877D,
        0x95CC3345DED552C2,
        0x5A92F1DBA88AD318,
        0x239900D4ED8623B9,
    ]

    assert h == res


def test_encoder():
    h = [
        0x0D4D1C983FA580BA,
        0xE9F6129FB697276A,
        0xB7C45A68142F214C,
        0xD1A2FFDB6FBB124B,
        0x2D79AB2A39C5877D,
        0x95CC3345DED552C2,
        0x5A92F1DBA88AD318,
        0x239900D4ED8623B9,
    ]

    d = struct.pack("<8Q", *h).hex().zfill(128)
    assert d == blake2b(b"abc").hexdigest()
