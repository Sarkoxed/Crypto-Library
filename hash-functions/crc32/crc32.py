class CRC32:
    def __init__(self):
        self.table = []
        self.poly = 0xEDB88320
        for i in range(256):
            c = i
            for j in range(8):
                if c & 1:
                    c = self.poly ^ (c >> 1)
                else:
                    c >>= 1
            self.table.append(c)

    def digest(self, msg: bytes) -> int:
        c = 0xFFFFFFFF
        u = msg
        for i in range(len(u)):
            idx = (c ^ u[i]) & 0xFF
            c = self.table[idx] ^ (c >> 8)
        return c ^ 0xFFFFFFFF
