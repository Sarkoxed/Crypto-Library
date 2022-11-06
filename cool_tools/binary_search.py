def binary_search(x, start):
    a = start
    b = a * 16
    steps = 0
    while a < b:
        r = remote(HOST, PORT)
        c = (a + b) // 2
        c1 = long_to_bytes(c)
        c1 = b64encode(c1).decode()
        try:
            dec = fetch(r, x, c1)
            a = c 
        except EOFError:
            b = c - 1
        print(a, b)
        steps += 1
        r.close()

        if a == b - 1:
            break
    print(steps)
    if a % 2 == 0:
        return b
    return a


