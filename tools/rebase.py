def rebase(n, b):
    if n < b:
        return [n]
    else:
        return [n % b] + rebase(n//b, b)
