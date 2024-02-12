from string import ascii_lowercase, ascii_uppercase, digits

alph = ascii_uppercase + ascii_lowercase + digits + "+/"


def base64encode(m: bytes):
    padlen = 0
    padding = ""
    if len(m) * 8 % 6 != 0:
        padding = "=" * (len(m) % 4)
        padlen = 6 - len(m) * 8 % 6
    b = "".join(bin(x)[2:].zfill(8) for x in m) + "0" * padlen
    blocks = [int(b[i : i + 6], 2) for i in range(0, len(b), 6)]
    enc = "".join(alph[i] for i in blocks) + padding
    return enc.encode()
