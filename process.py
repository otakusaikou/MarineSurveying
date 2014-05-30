#!/usr/bin/python2.7
import matplotlib.pyplot as plt
import bisect
import sys
from mpl_toolkits.mplot3d import Axes3D
from numpy import array, matrix, sqrt, set_printoptions

set_printoptions(suppress = True)

#read GPS data
def readGPS(filename):
    fin = open(filename)
    data = fin.read()
    T = map(lambda x: float(x.split(",")[0]), data.split()[1:])
    lat = map(lambda x: float(x.split(",")[8]) / 100, data.split()[1:])
    lon = map(lambda x: float(x.split(",")[10]) / 100, data.split()[1:])
    fin.close()
    return T, lat, lon

def readHVE(filename):
    fin = open(filename)
    data = fin.read()[:-1]
    T = map(lambda x: float(x.split(",")[0]), data.split("\r\n"))
    dz = map(lambda x: float(x.split(",")[1]), data.split("\r\n"))
    fin.close()
    return T, dz
    
def readSB(filename):
    fin = open(filename)
    data = fin.read()[:-1]
    T = map(lambda x: float(x.split(",")[0]), data.split("\r\n"))
    z = map(lambda x: float(x.split(",")[1]), data.split("\r\n"))

    fin.close()
    return T, z

def getLatLon(data, t):
    index = bisect.bisect_left(data[0], t)
    lat = ((data[1][index]) * (data[0][index + 1] - t) + (data[1][index + 1]) * (t - data[0][index])) / (data[0][index + 1] - data[0][index])
    lon = ((data[2][index]) * (data[0][index + 1] - t) + (data[2][index + 1]) * (t - data[0][index])) / (data[0][index + 1] - data[0][index])
    return lat, lon

def plot2DLine(T, x, y, xlabel = "longtitude", ylabel = "latitude", figname = "figure"):
    fig = plt.figure(figname)    
    plt.plot(x, y, 'b*')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

def plot3DSurface(x, y, z, xlabel = "longtitude", ylabel = "latitude", zlabel = "depth", figname = "figure"):
    fig = plt.figure(figname)
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_trisurf(x, y, z, linewidth=1, color='r', cmap=plt.cm.CMRmap)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)

def main():
    T, lat, lon = readGPS("14052309.GGA")
    T2, dz = readHVE("14052309.HVE")
    T3, z = readSB("14052309.SB")

    x3D = []
    y3D = []
    z3D = []
    #filtering blunders
    z_mean = sum(z)/len(z)
    z_sigma = sqrt((array(z)**2).sum() / len(z))
    z_1 = []
    T3_1 = []
    for i in range(len(T3)):
        if abs(z[i] - z_mean) < z_sigma and z[i] > 0:
            z_1.append(z[i])
            T3_1.append(T3[i])
    T3 = T3_1
    z = z_1
    for i in range(len(T3)):
        if z[i] == 0:
            continue
        p, l = getLatLon(array([T, lat, lon]), T3[i])
        x3D.append(l)
        y3D.append(p)
        z3D.append(z[i])
        if i > 10000:
            break
        sys.stdout.write("%2d%%" % int(1.0 * i / 100))
        sys.stdout.write("\b"*3)


    #plot3DSurface(x3D, y3D, z3D)    
    #plt.show()
    #plot2DLine(T, lon, lat, figname = "track")
    #plot2DLine(T2, dz, T2, figname = "delta-z")
    #plot2DLine(T3_1, T3_1, z_1, "time", "depth", "depth")
    plot2DLine(T, x3D, y3D, "time", "depth")
    plt.show()
    return 0

if __name__ == "__main__":
    main()
