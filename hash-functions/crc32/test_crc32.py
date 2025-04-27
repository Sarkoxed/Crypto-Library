import pytest
from sage.all import vector
import os
import random
import binascii
from crc32 import CRC32
from crc32_attacks import (
    to_vec,
    to_int,
    get_lin_op,
    linearized_crc32,
    algebraized_crc32,
)


def get_msg(n):
    for _ in range(n):
        yield os.urandom(random.randint(1, 1000))


@pytest.mark.parametrize("m", get_msg(1000))
def test_crc32(m):
    hasher = CRC32()
    assert binascii.crc32(m) == hasher.digest(m)


def test_linearized_table():
    hasher = CRC32()
    table = hasher.table

    for i in range(256):
        op = to_vec(i)
        lhs = table[i]
        rhs = to_int(get_lin_op() * op)
        assert lhs == rhs


@pytest.mark.parametrize("m", get_msg(100))
def test_lin_crc32(m):
    assert binascii.crc32(m) == linearized_crc32(m)


@pytest.mark.parametrize("m", get_msg(100))
def test_alg_crc32(m):
    assert binascii.crc32(m) == algebraized_crc32(m)
