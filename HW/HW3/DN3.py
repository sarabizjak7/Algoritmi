# DN 3 Algoritmi
#----------------------
# nal 1, primer c
#-----------------------
import numpy as np


#pomožna funkcija, ki ugotovi ali je left ali right turn
def direction(p):
    p0 = p[0]
    p1 = p[1]
    p2 = p[2]
    v1x = p1[0] - p0[0]
    v1y = p1[1] - p0[1]
    v2x = p2[0] - p1[0]
    v2y = p2[1] - p1[1]
    if v1x * v2y - v1y * v2x > 0.0:
        return 'L'
    else:
        return 'R'

def find_upper(coord_list):
    upper = coord_list[:2]
    for i in range(2, len(coord_list)):
        upper += [coord_list[i]]
        while len(upper) > 2 and direction(upper[-3:]) != 'L':
            upper = upper[:-2] + [upper[-1]]
    return upper

def find_lower(coord_list):
    #print("lower COORd")
    #print(coord_list)
    lower = coord_list[:2]
    for i in range(2, len(coord_list)):
        lower += [coord_list[i]]
        while len(lower) > 2 and direction(lower[-3:]) != 'L':
            lower = lower[:-2] + [lower[-1]]
    return lower


def ortogonals(c1x, c1y, c2x, c2y):
    ort = []
    for i in range(len(c1x)-1):
        ex = c1x[i+1] - c1x[i]
        ey = c1y[i+1] - c1y[i]
        ort += [(-ey,ex)]
    ort += [(c1y[-1]-c1y[0], c1x[0] - c1x[-1])]

    for i in range(len(c2x)-1):
        ex = c2x[i+1] - c2x[i]
        ey = c2y[i+1] - c2y[i]
        ort += [(-ey,ex)]
    ort += [(c2y[-1]-c2y[0], c2x[0] - c2x[-1])]

    return ort

#pomožna funkcija za detetkcijo presečišča
def intersect(c1x, c1y, c2x, c2y):
    ort = ortogonals(c1x, c1y, c2x, c2y)
    #sprehodi se čez vse ort
    for el in ort:
        #poglej če se intervala sekata
        proj1 = []
        proj2 = []
        
        #make all projections in p1
        for i in range(len(c1x)): 
            p = np.dot([c1x[i], c1y[i]], el)
            proj1 += [p]
        
        min1 = min(proj1)
        max1 = max(proj1)

        #make all projections in p2
        for i in range(len(c2x)): 
            p = np.dot([c2x[i], c2y[i]], el)
            proj2 += [p]
        
        min2 = min(proj2)
        max2 = max(proj2)

        if min1 <= max2 and min2 <= max1:
            ort = True
        else:
            return False

    return ort






#print("FIND LOWER")
#print(find_lower([(0.0, 0.0), (2.5, 0.0), (3.0, 0.0), (4.0, -1.0), (5.0, 0.0)]))
#print("find upper")
#print(find_upper([(5.0, 0.0), (4.0, 1.0), (3.0, 0.0), (2.5, 0.0), (2.0, 1.5), (0.0, 1.5), (0.0, 0.0)]))


def unija_in_presek(file):
    with open(file, 'r') as f:
        data = f.readlines()
        sez = []
        for line in data:
            floats =  [float(x) for x in line.split()]
            sez.append(floats)
        #naredimo sezname koordinat točk
        x1 = sez[0]
        y1 = sez[1]
        x2 = sez[2]
        y2 = sez[3]

        #združimo v eno zgornjo in spodnjo pot
        max1 = x1.index(max(x1))
        max2 = x2.index(max(x2))

        #print(x1)
        #print(x2)
        upper_x = x1[max1:]+ [x1[0]] + x2[max2:] + [x2[0]]
        #print(upper_x)
        lower_x = x1[:max1+1] + x2[:max2+1]
        upper_y = y1[max1:]+ [y1[0]] + y2[max2:] + [y2[0]]
        lower_y = y1[:max1+1] + y2[:max2+1]
        upper = list(zip(upper_x,upper_y))
        upper.sort(reverse=True)
        lower = list(zip(lower_x, lower_y))
        lower.sort()
        print("--------------------")
        print(upper)
        print(lower)
        print("--------------------")
        
        #naredimo ovojnico
        hull1 = find_lower(lower) 
        hull2 = find_upper(upper)
        print("--------------------")
        print(hull1)
        print(hull2)
        print("--------------------")
        
        hull = hull1[:-1] + hull2[:-1]
        res = list(zip(*hull))
        x = list(res[0])
        y = list(res[1])
        for i in range(len(x)):
            if x[i].is_integer():
                x[i] = int(x[i])
            if y[i].is_integer():
                y[i] = int(y[i])
        print(*x)
        print(*y)

        #izračunamo presečišče
        detect_intersect = intersect(x1,y1,x2,y2)
        print(detect_intersect)

unija_in_presek("vhod.txt") 

