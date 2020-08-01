import numpy as np
import math
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import multivariate_normal

def plot_FNoKS():
    x = ["Original", "7 ", "9", "11"]
    xp = np.arange(len(x))
    y1 = [88, 118, 120, 109]
    plt.title("Difference of Kernel Size")
    plt.xlabel("Kernel Size")
    plt.ylabel("Difference of Feature Number")
    width = 0.4
    plt.bar([i for i in xp], y1, width=width, label = "Difference", hatch = "---", color = "#FFFFFF", edgecolor = "C1")
    plt.xticks(xp, x)
    plt.legend()
    plt.show()

def plot_IRRoFN():
    x = ["1000", "900", "800", "700", "600", "500", "400", "300", "200", "100"]
    xp = np.arange(len(x))
    y1 = [54 / 56 * 100, 53 / 56 * 100, 53 / 56 * 100, 47 / 56 * 100, 47 / 56 * 100, 46 / 56 * 100, 37 / 56 * 100, 36 / 56 * 100, 23 / 56 * 100, 9 / 56 * 100]
    y2 = [51 / 56 * 100, 52 / 56 * 100, 48 / 56 * 100, 50 / 56 * 100, 46 / 56 * 100, 46 / 56 * 100, 35 / 56 * 100, 29 / 56 * 100, 7 / 56 * 100, 7 / 56 * 100]
    plt.title("Image Recognition Rate of Feature Number")
    plt.xlabel("Feature Number")
    plt.ylabel("Image Recognition Rate (%)")
    plt.plot(y1, label = "Original", marker = "D", color = "C2")
    plt.plot(y2, label = "Cropped", marker = "o", color = "C1")
    plt.xticks(xp, x)
    plt.legend()
    plt.show()

def plot_TCoFN():
    x = ["1000", "900", "800", "700", "600", "500", "400", "300", "200", "100"]
    xp = np.arange(len(x))
    y1 = [15.55, 13.94, 12.28, 10.63, 9.06, 7.51, 5.91, 4.39, 2.83, 1.44]
    y2 = [3.91, 3.39, 2.87, 2.56, 2.31, 2.21, 1.61, 1.24, 1.08, 0.55]
    plt.title("Time Cost of Feature Number")
    plt.xlabel("Feature Number")
    plt.ylabel("Time Cost (s)")
    plt.plot(y1, label = "Original", marker = "D", color = "C2")
    plt.plot(y2, label = "Cropped", marker = "o", color = "C1")
    plt.xticks(xp, x)
    plt.legend()
    plt.show()

def plot_IRRwIC():
    x = ["A", "B", "C"]
    xp = np.arange(len(x))
    y1 = [17 / 72 * 100, 8 / 75 * 100, 18 / 57 * 100]
    y2 = [50 / 56 * 100, 48 / 50 * 100, 40 / 50 * 100]
    plt.title("Image Recognition Rate with Image Cropping")
    plt.xlabel("Users")
    plt.ylabel("Image Recognition Rate (%)")
    width = 0.4
    plt.bar([i - width / 2 for i in xp], y1, width=width, label = "w/o Assess/Pre", hatch = "...", color = "#FFFFFF", edgecolor = "C1")
    plt.bar([i + width / 2 for i in xp], y2, width=width, label = "with Assess/Pre", hatch = "////", color = "#FFFFFF", edgecolor = "C2")
    plt.xticks(xp, x)
    axes = plt.gca()
    axes.set_ylim([0, 100])
    plt.legend()
    plt.show()

def plot_IRRwoIC():
    x = ["A", "B", "C"]
    xp = np.arange(len(x))
    y1 = [56 / 72 * 100, 54 / 75 * 100, 36 / 57 * 100]
    y2 = [47 / 56 * 100, 49 / 50 * 100, 37 / 50 * 100]
    plt.title("Image Recognition Rate w/o Image Cropping")
    plt.xlabel("Users")
    plt.ylabel("Image Recognition Rate (%)")
    width = 0.4
    plt.bar([i - width / 2 for i in xp], y1, width=width, label = "w/o Assess/Pre", hatch = "...", color = "#FFFFFF", edgecolor = "C1")
    plt.bar([i + width / 2 for i in xp], y2, width=width, label = "with Assess/Pre", hatch = "////", color = "#FFFFFF", edgecolor = "C2")
    plt.xticks(xp, x)
    axes = plt.gca()
    axes.set_ylim([0, 100])
    plt.legend()
    plt.show()

def plot_TCoIR():
    x = ["A", "B", "C"]
    xp = np.arange(len(x))
    y1 = [10.63, 10.89, 10.81]
    y2 = [2.56, 3.00, 3.08]
    plt.title("Time Cost of Image Recognition")
    plt.xlabel("Users")
    plt.ylabel("Time Cost (s)")
    width = 0.4
    plt.bar([i - width / 2 for i in xp], y1, width=width, label = "Original", hatch = "...", color = "#FFFFFF", edgecolor = "C1")
    plt.bar([i + width / 2 for i in xp], y2, width=width, label = "Cropped", hatch = "////", color = "#FFFFFF", edgecolor = "C2")
    plt.xticks(xp, x)
    axes = plt.gca()
    axes.set_ylim([0, 13])
    plt.legend()
    plt.show()

def Gaussian_Distrubution():
    x, y = np.mgrid[-1.0:1.0:30j, -1.0:1.0:30j]
    xy = np.column_stack([x.flat, y.flat])
    mu = np.array([0, 0])
    sigma = np.array([.5, .5])
    covariance = np.diag(sigma ** 2)
    z = multivariate_normal.pdf(xy, mean = mu, cov = covariance)
    z = z.reshape(x.shape)
    figure = plt.figure()
    axe = figure.add_subplot(111, projection = "3d")
    axe.plot_surface(x, y, z, alpha = 1, color = "#FFFFFF", edgecolor = "#000000")
    axe.set_xlabel("X")
    axe.set_ylabel("Y")
    axe.set_zlabel("Pixel Value")
    plt.show()

def unique():
    x = [14, 14, 15, 16, 18, 15, 11, 12, 12, 12, 13, 14, 15, 14, 12, 15, 13, 13, 16, 14, 15, 14, 12, 12, 16, 13, 13, 13, 14, 12, 14, 15, 15, 13, 14, 13, 13, 17, 12, 16, 12, 12, 13, 13, 14, 13, 13, 13, 14, 15, 13, 13, 13, 14, 13, 12, 14, 11, 14, 13, 14, 16, 14, 15, 15, 14, 12, 12, 12, 13, 12, 12, 15, 14, 14, 16, 13, 15, 13, 17, 14, 13, 14, 15, 13, 12, 13, 15, 14, 15, 13, 11, 18, 14, 14, 14, 15, 14, 13, 14, 13, 13, 14, 13, 15, 16, 15, 15, 14, 18, 18, 15, 13, 12, 13, 14, 12, 14, 14, 14, 13, 18, 15, 15, 13, 14, 12, 13, 13, 19, 16, 15, 15, 13, 13, 15, 13, 14, 14, 14, 13, 13, 14, 14, 13, 14, 14, 14, 12, 16, 15, 16, 12, 12, 13, 16, 17, 13, 14, 14, 12, 13, 13, 13, 15, 13, 14, 15, 13, 13, 13, 14, 13, 17, 14, 13, 16, 12, 15, 13, 12, 14, 13, 12, 13, 14, 14, 12, 14, 16, 13, 12, 13, 13, 13, 15, 15, 14, 14, 12, 13, 13, 13, 14, 18, 13, 15, 14, 12, 13, 12, 13, 15, 12, 16, 15, 15, 14, 13, 15, 13, 18, 13, 14, 13, 15, 14, 13, 15, 12, 14, 16, 14, 13, 12, 13, 13, 15, 14, 14, 14, 13, 14, 13, 14, 14, 15, 15, 14, 14, 14, 16, 13, 12, 13, 15, 14, 15, 14, 12, 15, 12, 13, 15, 14, 13, 15, 13, 15, 15, 14, 15, 13, 15, 15, 15, 12, 11, 14, 12, 14, 13, 13, 14, 13, 13, 12, 12, 11, 13, 18, 14, 14, 15, 13, 14, 13, 13, 17, 14, 13, 15, 14, 14, 14, 14, 12, 13, 15, 13, 13, 13, 13, 13, 13, 13, 12, 13, 14, 16, 13, 12, 11, 18, 13, 14, 13, 15, 13, 13, 13, 13, 12, 13, 13, 17, 13, 16, 12, 14, 13, 17, 14, 12, 16, 14, 13, 15, 13, 14, 12, 15, 13, 13, 12, 14, 13, 14, 17, 13, 14, 17, 14, 14, 12, 14, 13, 13, 13, 12, 15, 13, 15, 12, 14, 14, 14, 15, 12, 13, 12, 14, 15, 12, 15, 17, 13, 14, 14, 13, 15, 16, 12, 16, 13, 14, 13, 12, 13, 14, 15, 14, 16, 14, 14, 13, 13, 12, 12, 14, 15, 16, 14, 15, 14, 14, 14, 13, 14, 13, 13, 15, 13, 18, 14, 15, 16, 12, 13, 13, 12, 15, 12, 13, 12, 13, 14, 12, 14, 13, 14, 12, 13, 13, 16, 14, 16, 15, 14, 17, 14, 13, 12, 16, 12, 14, 15, 16, 13, 14, 13, 14, 15, 15, 15, 13, 13, 13, 12, 13, 12, 15, 13, 14, 13, 15, 14, 14, 15, 14, 13, 13, 14, 14, 12, 16, 13, 13, 13, 19, 15, 13, 14, 13, 14, 16, 16, 13, 14, 14, 15, 14, 14, 15, 14, 13, 12, 15, 14, 12, 13, 13, 14, 12, 16, 13, 13, 13, 16, 17, 15, 13, 14, 14, 13, 12, 15, 14, 14, 12, 15, 14, 13, 14, 14, 15, 17, 12, 16, 15, 14, 15, 13, 14, 15, 14, 13, 13, 13, 13, 13, 13, 15, 12, 13, 15, 12]
    plt.title("Uniqueness of Database")
    plt.xlabel("Tile's ID")
    plt.ylabel("Matched Features")
    plt.plot(x, label = "Highest Matched Features", color = "red")
    axes = plt.gca()
    axes.set_ylim([0, 100])
    plt.legend()
    plt.show()

def ideal():
    x = ["Samsung A60", "Sony Xperial II 10"]
    xp = np.arange(len(x))
    y1 = [96, 98]
    plt.title("Image Recognition Rate")
    plt.xlabel("Phone Model")
    plt.ylabel("Image Recognition Rate (%)")
    plt.bar([i for i in xp], y1, width = 0.3, hatch = "xxxx", color = "#FFFFFF", edgecolor = "tab:blue")
    plt.xticks(xp, x)
    axes = plt.gca()
    axes.set_ylim([0, 100])
    plt.legend()
    plt.show()

if __name__ == "__main__":
    plot_FNoKS()