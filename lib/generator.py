
def generators(n):
    s = set(range(1, n))
    results = []
    for a in s:
        g = set()
        for x in s:
            tmp = (a**x) % n
            if tmp not in g:
                g.add(tmp)
            else:
                break
        if g == s:
            results.append(a)
        if len(results) == 1:
            break
    return results

def main():    
    p = 16798108731015832284940804142231733909759579603404752749028378864165570215949
    #p = 1021
    gens = generators(p)
    if gens:
        print(f"Z_{p} has generators {gens}")
        print(len(gens))

if __name__ == '__main__':
    main()
