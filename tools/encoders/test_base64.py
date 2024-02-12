import pytest
from os import urandom
from base64 import b64encode
from random import randint

from base64e import base64encode


def get_msg(n):
    for _ in range(n):
        yield urandom(randint(1, 100))


@pytest.mark.parametrize("m", get_msg(100))
def test_base64_encode_no_pad(m):
    assert base64encode(m).strip(b"=") == b64encode(m).strip(b"=")
