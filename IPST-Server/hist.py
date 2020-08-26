from cv2 import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np 
import glob

def hist(filename):
    image1 = cv.imread("temp\\match\\smooth9\\1\\" + filename + ".png", cv.IMREAD_GRAYSCALE)
    image2 = cv.imread("temp\\match\\smooth9\\2\\" + filename + ".png", cv.IMREAD_GRAYSCALE)
    image3 = cv.imread("temp\\match\\smooth9\\3\\" + filename + ".png", cv.IMREAD_GRAYSCALE)
    image4 = cv.imread("temp\\match\\smooth9\\4\\" + filename + ".png", cv.IMREAD_GRAYSCALE)
    image5 = cv.imread("temp\\match\\smooth9\\5\\" + filename + ".png", cv.IMREAD_GRAYSCALE)

    hist1 = cv.calcHist(image1, [0], None, [256], [0, 256])
    hist2 = cv.calcHist(image2, [0], None, [256], [0, 256])
    hist3 = cv.calcHist(image3, [0], None, [256], [0, 256])
    hist4 = cv.calcHist(image4, [0], None, [256], [0, 256])
    hist5 = cv.calcHist(image5, [0], None, [256], [0, 256])
    plt.plot(hist1, label = "1")
    plt.plot(hist2, label = "2")
    plt.plot(hist3, label = "3")
    plt.plot(hist4, label = "4")
    plt.plot(hist5, label = "5")
    plt.legend()
    plt.show()
    print(hist1[160])
    #print(hist3)
    #print(hist4)
    #print(hist5)

if __name__ == "__main__":
    hist("153844")