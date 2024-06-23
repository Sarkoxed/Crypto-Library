from Crypto.Cipher import DES
from os import urandom

weak_keys = [
    bytes.fromhex("0101010101010101"),
    bytes.fromhex("0000000000000000"),
    bytes.fromhex("FEFEFEFEFEFEFEFE"),
    bytes.fromhex("FFFFFFFFFFFFFFFF"),
    bytes.fromhex("E0E0E0E0F1F1F1F1"),
    bytes.fromhex("E1E1E1E1F0F0F0F0"),
    bytes.fromhex("1F1F1F1F0E0E0E0E"),
    bytes.fromhex("1E1E1E1E0F0F0F0F"),
]

for key in weak_keys:
    cip = DES.new(key=key, mode=DES.MODE_ECB)
    m = urandom(8)
    c = cip.encrypt(m)
    d = cip.encrypt(c)
    assert d == m


semi_weak_keys = [
    (bytes.fromhex("011F011F010E010E"), bytes.fromhex("1F011F010E010E01")),
    (bytes.fromhex("01E001E001F101F1"), bytes.fromhex("E001E001F101F101")),
    (bytes.fromhex("01FE01FE01FE01FE"), bytes.fromhex("FE01FE01FE01FE01")),
    (bytes.fromhex("1FE01FE00EF10EF1"), bytes.fromhex("E01FE01FF10EF10E")),
    (bytes.fromhex("1FFE1FFE0EFE0EFE"), bytes.fromhex("FE1FFE1FFE0EFE0E")),
    (bytes.fromhex("E0FEE0FEF1FEF1FE"), bytes.fromhex("FEE0FEE0FEF1FEF1")),
]

for key1, key2 in semi_weak_keys:
    cip1 = DES.new(key=key1, mode=DES.MODE_ECB)
    cip2 = DES.new(key=key2, mode=DES.MODE_ECB)
    m = urandom(8)

    c1 = cip1.encrypt(m)
    c2 = cip2.encrypt(c1)
    assert c2 == m

    c1 = cip2.encrypt(m)
    c2 = cip1.encrypt(c1)
    assert c2 == m
