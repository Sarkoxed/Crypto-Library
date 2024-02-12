import pytest
from os import urandom
from Crypto.Cipher import ChaCha20 as chacha20
from random import randrange

from chacha20 import ChaCha20
from reverse import quarter_round, reverse_quarter_round


def test_quarter_round():
    a = 0x11111111
    b = 0x01020304
    c = 0x9B8D6F43
    d = 0x01234567

    a, b, c, d = ChaCha20.quarter_round(a, b, c, d)
    assert a == 0xEA2A92F4
    assert b == 0xCB1CF8CE
    assert c == 0x4581472E
    assert d == 0x5881C4BB


def test_init():
    key = bytes(range(32))
    nonce = b"\x00\x00\x00\x09\x00\x00\x00\x4a\x00\x00\x00\x00"

    cipher = ChaCha20(key, nonce, counter=1)
    test_state = [
        0xE4E7F110,
        0x15593BD1,
        0x1FDD0F50,
        0xC47120A3,
        0xC7F4D1C7,
        0x368C033,
        0x9AAA2204,
        0x4E6CD4C3,
        0x466482D2,
        0x9AA9F07,
        0x5D7C214,
        0xA2028BD9,
        0xD19C12B5,
        0xB94E16DE,
        0xE883D0CB,
        0x4E3C50A2,
    ]

    assert cipher.block() == test_state


def test_chach20_encrypt():
    key = bytes(range(32))
    nonce = b"\x00\x00\x00\x00\x00\x00\x00\x4a\x00\x00\x00\x00"

    cipher = ChaCha20(key, nonce, counter=1)

    pt = b"Ladies and Gentlemen of the class of '99: If I could offer you only one tip for the future, sunscreen would be it."
    ct = cipher.encrypt(pt)
    assert (
        ct
        == b"n.5\x9a%h\xf9\x80A\xba\x07(\xdd\ri\x81\xe9~z\xec\x1dC`\xc2\n'\xaf\xcc\xfd\x9f\xae\x0b\xf9\x1be\xc5RG3\xab\x8fY=\xab\xcdb\xb3W\x169\xd6$\xe6QR\xab\x8fS\x0c5\x9f\x08a\xd8\x07\xca\r\xbfP\rjaV\xa3\x8e\x08\x8a\"\xb6^R\xbcQM\x16\xcc\xf8\x06\x81\x8c\xe9\x1a\xb7y76Z\xf9\x0b\xbft\xa3[\xe6\xb4\x0b\x8e\xed\xf2x^B\x87M"
    )


def gen_params(n):
    for i in range(1, n):
        key = urandom(32)
        nonce = urandom(12)
        yield key, nonce, i


@pytest.mark.parametrize("key, nonce, pt_len", gen_params(1000))
def test_chacha20_arb_encrypt(key, nonce, pt_len):
    chacha_own = ChaCha20(key, nonce, counter=0)
    chacha_for = chacha20.new(key=key, nonce=nonce)

    r = b"\x00" * pt_len
    assert chacha_own.encrypt(r) == chacha_for.encrypt(r)

@pytest.mark.parametrize("a, b, c, d", [(randrange(0, 2**32), randrange(0, 2**32), randrange(0, 2**32), randrange(0, 2**32))])
def test_reverse(a, b, c, d):
    assert (a, b, c, d) == reverse_quarter_round(*quarter_round(a, b, c, d))
