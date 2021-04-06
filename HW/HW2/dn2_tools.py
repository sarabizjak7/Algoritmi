
#### ALGORITMI, DN2 ####
### POMOZNE FUNKCIJE ###

# Definirajmo delta funkcijo:

delta= [[1, 0, 0, 0],
    [2, 0, 0, 0],
    [2, 3, 3, 0],
    [4, 0, 0, 0],
    [2, 5, 0, 0],
    [1, 0, 0, 6],
    [1, 0, 0, 0]]

def najdi_vse_pojavitve(s):
    """
    S pomočjo avtomata (delta funkcija) najde in vrne lokacije vseh pojavitev vzorcev AAUAUG in AACAUG.
    Izhod je seznam  elementov (zacetek, konec), kjer je zacetek indeks, kjer se pojavitev zacne, in konec, kjer se konca.
    """
    # stanja označimo 0, 1, 2, 3, 4, 5, 6, kjer 0 začetno stanje
    stanje = 0
    pojavitve = []
    # definiramo A = 0, U = 1, C = 2, G = 3 za iskanje po stolpcih stanj
    vhod = {'A':0, 'U':1, 'C':2, 'G':3}
    for i in range(len(s)):
        # definiramo novo stanje:
        stanje = delta[stanje][vhod[s[i]]]
        # če pridemo v stanje 6, potem smo dobili pojavitev:
        if stanje == 6:
            pojavitve.append((i - 5, i))
    return pojavitve

"""
# Osnovna primera:
primer1 = najdi_vse_pojavitve('AAUAUG')
primer2 = najdi_vse_pojavitve('AACAUG')

print("Osnovna primera: ")
print(primer1)
print(primer2)

print("-----------------------------------")
print("-----------------------------------")
"""

with open('generated_genome.txt', 'r') as g:
    genom = g.readline().replace('\n', '')
generated = najdi_vse_pojavitve(genom)
print(generated)