def factor(n):
    j = 2
    ans = []
    local = [j, 0]
    while(1):
        if(n % j == 0):
            n //= j
            local[1] += 1
        else:
            if(local[1]):
                ans.append(tuple(local))
            if(j == 2):
                j += 1
            else:
                j += 2
            local = [j, 0]
            if(n == 1):
                break
    return ans

