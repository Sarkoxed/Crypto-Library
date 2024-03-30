from diff import (
    int_to_bin,
    delta_xor,
    delta_int_mod,
    delta_sub,
    sub_to_xor,
    sub_to_int_mod,
    xor_int_mod_to_sub,
)
import pytest
from random import randint


@pytest.mark.parametrize("k", range(1, 33))
def test(k):
    x1 = int_to_bin(randint(0, 2**k - 1), k)
    x2 = int_to_bin(randint(0, 2**k - 1), k)

    dX_xor = delta_xor(x1, x2)
    dX_mod = delta_int_mod(x1, x2)
    dX_sub = delta_sub(x1, x2)

    assert sub_to_xor(dX_sub) == dX_xor
    assert sub_to_int_mod(dX_sub) == dX_mod
    assert dX_sub in xor_int_mod_to_sub(dX_xor, dX_mod)
