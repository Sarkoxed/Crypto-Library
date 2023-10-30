from sha1_foreighn import Sha1Hash
import struct


def pad(m):
    mes_length = len(m)
    m += b"\x80"
    m += b"\x00" * ((56 - (mes_length + 1) % 64) % 64)

    message_bit_length = mes_length * 8
    m += struct.pack(b">Q", message_bit_length)
    return m


def length_extension_attack(previous_hash, known_length):
    s = Sha1Hash()
    h = [int(previous_hash[i : i + 8], 16) for i in range(0, len(previous_hash), 8)]
    s._h = h
    s._message_byte_length = known_length
    s.update(b"aboba")
    return s.hexdigest()


m = b"kek"
h1 = Sha1Hash().update(m).hexdigest()

res1 = length_extension_attack(h1, len(pad(m)))
res2 = Sha1Hash().update(pad(m) + b"aboba").hexdigest()

print(res1 == res2)
