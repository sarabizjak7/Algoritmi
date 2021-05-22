def modularnoPotenciranje(a, b, n):
    """
    Vhod: a, b, n
    Izhod: a^b mod n
    """

    if b == 0:
        return 1

    d = 1 # za mnozenja pri lihih bitih
    # osnova po mod n, ki jo na vsakem koraku kvadriramo
    osnova = a % n       
    while b > 1:
        # trenutni bit liho stevilo
        if b % 2 == 1:       
            d = (osnova * d) % n
            b = b // 2
            osnova = (osnova ** 2) % n
        # trenutni bit sodo stevilo
        else:
            b = b // 2
            osnova = (osnova ** 2) % n

    osnova = (osnova * d) % n
    return osnova


"""
#( TESTI )#

# Primer iz ucbenika
a = 7
b = 560
n = 561
print(modularnoPotenciranje(a, b, n))
print((a ** b) % n)

a1 = 106
b1 = 178
n1 = 908
print(modularnoPotenciranje(a1, b1, n1))
print((a1 ** b1) % n1)

a2 = 1063
b2 = 128
n2 = 1819
print(modularnoPotenciranje(a2, b2, n2))
print((a2 ** b2) % n2)

a3 = 106
b3 = 0
n3 = 908
print(modularnoPotenciranje(a3, b3, n3))
print((a3 ** b3) % n3)
"""