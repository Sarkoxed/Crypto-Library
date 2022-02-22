from string import ascii_lowercase, ascii_uppercase, punctuation
s = input("insert a string: ")
for(i in range(26)):
    a = ascii_lowercase[i:] + ascii_lowercase[:i]
    b = ascii_uppercase[i:] + ascii_uppercase[:i]
    z = dict(zip(a+b+punctuation, ascii_lowercase+ascii_uppercase + punctuation))
    print("".join([z[x] for x in s]))
    
    
