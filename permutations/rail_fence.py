def known_N(s: str, n: int, sep=" "):
    ans = []
    j = 0
    flag = True
    for i in range(1, n+1):
        dist1 = 2*n - 1 - 2*i
        dist2 = 2*i - 3
        ans.append(sep*(i-1))
        while(len(ans[i-1]) < len(s) and j < len(s)):
            if(flag and dist1 > 0):
                ans[i-1] = ans[i-1] + s[j] + dist1 * sep
                j+=1 
            elif(not flag and dist2 > 0):
                ans[i-1] = ans[i-1] + s[j] + dist2 * sep
                j+=1

            flag = not flag
                

        print(ans[i-1])
        flag = True

def unknown_N(s: str):
    for i in range(2, len(s)):
        known_N(s, i)
        print()

def main():
    n = int(input("N-> "))
    s = input("S-> ")
    print(s)
    known_N(s, n)

    #unknown_N(s)


if __name__ == "__main__":
    main()


