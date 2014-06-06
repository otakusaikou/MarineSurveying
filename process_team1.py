#!/usr/bin/python2.7
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import ScalarFormatter
from numpy import array, sqrt, set_printoptions, matrix, arange, meshgrid, ravel

#disable scientific notation of numpy 
set_printoptions(suppress = True)
       
def plot2DLine(x, y, threshold, xlabel = "x", ylabel = "y", figname = "figure", title = "Track", equal = False):
    fig = plt.figure(figname)
    ax = fig.add_subplot(111)
    start = 0
    
    #set x and y axis to equal
    if equal:
        ax.axis('equal')
        
    #break lines if range of two point bigger than threshold
    for i in range(len(x) - 1):
        if sqrt((x[i] - x[i + 1])**2 + (y[i] - y[i + 1])**2) > threshold:
            ax.plot(x[start:i + 1], y[start:i + 1], 'r*')
            start = i + 1
    ax.plot(x[start:], y[start:], 'r*')
    
    
    #disable scientific notation of plot
    formatter = ScalarFormatter(useOffset=False)
    ax.yaxis.set_major_formatter(formatter)
    ax.xaxis.set_major_formatter(formatter)
    
    ax.set_title(title, size = 20)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid()
    
def plot3DSurface(x, y, z, xlabel = "x", ylabel = "y", zlabel = "depth", figname = "figure", title = "Surface"):
    fig = plt.figure(figname)
    ax = fig.gca(projection='3d')

    ax.auto_scale_xyz([x.min(), x.max()], [y.min(), y.max()], [z.min(), z.max()])
    ax.plot_trisurf(x, y, z, cmap=cm.jet, linewidth=0.2)
    #ax.scatter(x, y, z)
    #ax.plot_surface(x, y, z)

    #disable scientific notation of plot
    formatter = ScalarFormatter(useOffset=False)
    ax.yaxis.set_major_formatter(formatter)
    ax.xaxis.set_major_formatter(formatter)

    ax.set_title(title, size = 20)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    
def LS(X, Y, Z):
    A = matrix([X**2 * Y**2, X**2, X**2 * Y, X * Y**2, X * Y, Y**2, X, Y]).T
    L = matrix(Z).T
    
    X = ((A.T * A).I) * (A.T * L)
    Q = (A.T * A).I
    V = A * X - L
    
    return X, Q, V

def getZ(x, y, param):
    X = matrix([x**2 * y*2, x**2, x**2 * y, x * y**2, x * y, y**2, x, y]).T
    print (param.T * X)[0, 0]
    return (param.T * X)[0, 0]

def main():
    #fin = open("coordinates_line_fixed.dat")
    fin = open("coordinates_height_fixed.dat")
    #fin = open("coordinates.txt")
    #fin = open("coordinates_all.txt")
    lines = fin.read().split("\n")[1:-1]
    data = array(map(lambda x: array(x.split(",")).astype(float), lines))
    X = data[:, 0]
    Y = data[:, 1]
    Z = data[:, 2]
    T = data[:, 3]
    
    #Xsur, Q, V = LS(X, Y, Z)
    
    #X = arange(X.min(), X.max(), 2)
    #Y = arange(Y.min(), Y.max(), 2)
    #X, Y = meshgrid(X, Y)
    #Z = array([getZ(x, y, Xsur) for x, y in zip(ravel(X), ravel(Y))])
    #Z = Z.reshape(X.shape)



    #ignore data with depth equals to zero 
    #X = X[(Z < -4) & (Z > -15)]
    #Y = Y[(Z < -4) & (Z > -15)]
    #Z = Z[(Z < -4) & (Z > -15)]
    #T = T[(Z < -4) & (Z > -15)]
    
    #fout = open("coordinates_height_fixed.dat", "w")
    #fout.write("X\tY\tZ\tT\n")
    
    #for i in range(len(T)):
        #fout.write("%.8f,%.8f,%.8f,%.8f\n" % (X[i], Y[i], Z[i], T[i]))
    #fout.close()
    
    
    plot2DLine(X, Y, 20, figname = "Track", title = "Track", equal = True)
    #plot2DLine(Y, Z, 20, figname = "X-Z", title = "X-Z")
    plot2DLine(T, Z, 1, "time", "depth", figname = "Depth", title = "Depth", equal = True)
    plot3DSurface(X, Y, Z)
    plt.show()

    return 0

if __name__ == "__main__":
    main()
