#!/usr/bin/python2.7
import matplotlib.pyplot as plt
import bisect
import sys
from numpy import array, matrix, sqrt, set_printoptions, meshgrid, empty, append

set_printoptions(suppress = True)

#read GPS data
def readGPS(filename):
    fin = open(filename)
    data = fin.read()
    T = map(lambda x: float(x.split(",")[0]), data.split()[1:])
    x = map(lambda x: float(x.split(",")[2]), data.split()[1:])
    y = map(lambda x: float(x.split(",")[1]), data.split()[1:])
    fin.close()
    return T, x, y

def readHVE(filename):
    fin = open(filename)
    data = fin.readlines()
    T = map(lambda x: float(x.split(",")[0]), data)
    dz = map(lambda x: float(x.split(",")[1]), data)
    fin.close()
    return T, dz
    
def readSB(filename):
    fin = open(filename)
    data = fin.readlines()
    T = map(lambda x: float(x.split(",")[0]), data)
    z = map(lambda x: float(x.split(",")[1]), data)

    fin.close()
    return T, z

def getZ(data, t):
    left = bisect.bisect_left(data[0], t)
    if left == 0 or left > len(data[0]) - 1:
        return 0    
    while data[0][left] > t:
        if left == 0 or left > len(data[0]) - 1:
            return 0
        left -= 1
    right = left
    while data[0][right] < t:
        if right == 0 or right > len(data[0]) - 1:
            return 0
        right += 1
        
    if len(data[1][left:right]) == 0 or len(data[1][left:right]) == 1:
        z = data[1][left]
    else:
        z = (data[1][left:right]).mean()
    
    if data[0][left] > t or data[0][right] < t:
        print "ERROR!"

    return z
        
def plot2DLine(T, x, y, xlabel = "x", ylabel = "y", figname = "figure"):
    fig = plt.figure(figname)    
    plt.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

def main():
    T, x, y = readGPS("14052309.GGA")
    T2, dz = readHVE("14052309.HVE")
    T3, z = readSB("14052309.SB")
    
    #ignore track with motion bigger than -15 and smaller than -0.5
    Ti = empty(0)
    xi = empty(0)
    yi = empty(0)
    for i in range(len(x) - 1):
        try:
            if True:#(y[i + 1] - y[i]) / (x[i + 1] - x[i]) < -0.5 and (y[i + 1] - y[i]) / (x[i + 1] - x[i]) > -15:
                Ti = append(Ti, T[i])
                xi = append(xi, x[i])
                yi = append(yi, y[i])
        except:
            pass

    #ignore data with depth equals to zero 
    x3D = empty(0)
    y3D = empty(0)
    z3D = empty(0)
    T3D = empty(0)
    for i in range(len(Ti)):
        tmpZ = getZ(array([T3, z]), Ti[i]) + getZ(array([T2, dz]), Ti[i])
        if tmpZ == 0:
            continue
        T3D = append(T3D, Ti[i])
        x3D = append(x3D, xi[i])
        y3D = append(y3D, yi[i])
        z3D = append(z3D, tmpZ)
        
    fout = open("coordinates_all.txt", "w")
    fout.write("X\tY\tZ\tT\n")
    for i in range(len(T3D)):
        fout.write("%.3f\t%.3f\t%.3f\t%.8f\n" % (x3D[i], y3D[i], z3D[i], T3D[i]))
        
    fout.close()


    return 0

if __name__ == "__main__":
    main()
