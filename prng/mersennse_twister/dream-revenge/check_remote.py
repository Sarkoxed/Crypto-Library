from pwn import remote
host, port =  "vsc.tf", 5004
r = remote(host, port)
#r.sendline(b'1, {seed()}, ' + b'2' * 2000)
r.sendline(b"[1, 2, 3, 4, 5, 6]")
r.interactive()
