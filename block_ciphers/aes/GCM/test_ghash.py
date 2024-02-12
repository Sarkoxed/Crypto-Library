import pytest
from os import urandom
from random import randint
from Crypto.Cipher import AES

from ghash import GHASH


def get_params(n):
    for _ in range(n):
        key = urandom(16)
        iv = urandom(randint(1, 16))
        pt = urandom(randint(1, 100))
        additional_info = urandom(randint(1, 100))
        yield key, iv, pt, additional_info


@pytest.mark.parametrize("key, iv, pt, additional_info", get_params(10000))
def test_ghash(key, iv, pt, additional_info):
    cipher = AES.new(key, mode=AES.MODE_GCM, nonce=iv)
    cipher.update(additional_info)
    ct, tag = cipher.encrypt_and_digest(pt)

    gh = GHASH(key, iv)
    gh.update(additional_info, True)
    gh.update(ct, False)
    tag_own = gh.get_tag()
    assert tag_own == tag
