import pytest
from os import urandom
from random import randint

from md5 import MD5
from hashlib import md5


def get_msg(n):
    for _ in range(n):
        yield urandom(randint(1, 1000)).hex()


@pytest.mark.parametrize("m", get_msg(100))
def test_base64_encode_no_pad(m):
    m = bytes.fromhex(m)
    h1 = MD5()
    h1.update(m)
    d1 = h1.digest()
    d2 = md5(m).digest()
    assert d1 == d2
