#!/usr/bin/python2.7
import matplotlib.pyplot as plt
import bisect
import sys
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
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

def readHeight(filename):
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
    while data[0, left] > t:
        if left == 0:
            z = data[1, 0]
            return z
        elif left > len(data[0]) - 1:
            z = data[1, -1]
            return z
        left -= 1
    right = left
    while data[0, right] < t:
        if right == 0:
            z = data[1, 0]
            return z
        elif right > len(data[0]) - 1:
            z = data[1, -1]
            return z
        right += 1
    
    if data[0, left] > t or data[0, right] < t:
        print "ERROR!"        
        
    if data[0, left] == data[0, right] and data[0, left] == t:
        z = data[1, left]
        return z
    z = (data[1, right] * (t - data[0, left]) + data[1, left] * (data[0, right] - t)) / (data[0, right] - data[0, left])
    return z

def LS(A, L):
    m = len(A)
    X = array((A.T * A).I * (A.T * L))
    
    V = array(A * X - L)
    S = sqrt((V.T).dot(V)[0, 0] / (m - 5))
    return X, S

def func(X, S, x, y, phii):
    phi = X[0, 0] * x**2 + X[1, 0] * x * y + X[2, 0] * y**2 + X[3, 0] * x + X[4, 0] * y
    if abs(phii - phi) >= S:
        return phi
    else:
        return phii
        
def plot2DLine(T, x, y, xlabel = "x", ylabel = "y", figname = "figure"):
    fig = plt.figure(figname)    
    plt.plot(x, y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)


def main():
    T, x, y = readGPS("14052309.GGA")
    T2, dz = readHVE("14052309.HVE")
    T3, z = readSB("14052309.SB")
    T4, h = readHeight("height.dat")
    
    #ignore track with motion bigger than -15 and smaller than -0.5
    Ti = empty(0)
    xi = empty(0)
    yi = empty(0)
    for i in range(len(x) - 1):
        try:
            if (y[i + 1] - y[i]) / (x[i + 1] - x[i]) < -0.5 and (y[i + 1] - y[i]) / (x[i + 1] - x[i]) > -15:
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
        height = getZ(array([T4, h]), Ti[i])
        SB = getZ(array([T3, z]), Ti[i])
        HVE = getZ(array([T2, dz]), Ti[i])
        print "%.8f\t%.8f\t%.8f\t%.8f" % (height, SB, HVE, Ti[i])
        tmpZ = height - SB + HVE
        if tmpZ == 0:
            continue
        T3D = append(T3D, Ti[i])
        x3D = append(x3D, xi[i])
        y3D = append(y3D, yi[i])
        z3D = append(z3D, tmpZ)

    z_mean = z3D.mean()
    z_sigma = z3D.std()
    
    #fout = open("coordinates_all.dat", "w")
    #fout.write("X\tY\tZ\tT\n")
    #for i in range(len(T3D)):
        #fout.write("%.8f,%.8f,%.8f,%.8f\n" % (x3D[i], y3D[i], z3D[i], T3D[i]))
    #fout.close()
    
    
    
    #filtering blunders
    #x3D = x3D[abs(z3D - z_mean) < z_sigma]
    #y3D = y3D[abs(z3D - z_mean) < z_sigma]
    #z3D = z3D[abs(z3D - z_mean) < z_sigma]
    #T3D = T3D[abs(z3D - z_mean) < z_sigma]
    
    
    #A = matrix([x3D[:11]**2, x3D[:11] * y3D[:11], y3D[:11]**2, x3D[:11], y3D[:11]]).T
    #L = matrix(z3D[:11]).T
    
    #for i in range(len(x3D[11:]) - 11):
        #X, S = LS(A, L)
        #print z3D[i + 11]
        #z3D[i + 11] = func(X, S, x3D[i + 11], y3D[i + 11], z3D[i + 11])
        #print z3D[i + 11]
        #A = matrix([x3D[i + 1:i + 12]**2, x3D[i + 1:i + 12] * y3D[i + 1:i + 12], y3D[i + 1:i + 12]**2, x3D[i + 1:i + 12], y3D[i + 1:i + 12]]).T
        #L = matrix(z3D[i + 1:i + 12]).T
        #print z3D[i + 11]
        
    
        #denominator = len(T)
        #iter = 0
        #fout.write("%.8f %.8f %.8f\n" % (x3D[i], y3D[i], z3D[i]))
        
        #if int(1.0 * i / (denominator / 100)) > iter:
            #iter = int(1.0 * i / (denominator / 100))
            #sys.stdout.write("%2d%%" % iter)
#            sys.stdout.write("\b"*4)
            
    plot2DLine((T3D - 41782) * 1440, (T3D - 41782) * 1440, z3D, "time", "depth", "depth")
    plt.show()
    return 0

if __name__ == "__main__":
    main()
