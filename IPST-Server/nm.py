from cv2 import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
import feat
import glob
import pickle
import time

def croppedImageMatchFeatureDatabase(name, database_type, feature, filename):
    orb = cv.ORB_create(feature)
    bfm = cv.BFMatcher()

    image = cv.imread("temp\\match\\" + database_type + "\\r\\" + name, cv.IMREAD_GRAYSCALE) # grayscale testing
    _, destination = orb.detectAndCompute(image, None) # read image
    database = pickle.load(open("database\\store\\" + database_type + "_database.p", "rb")) # read database

    txt = open(filename + ".txt", "a")
    txt.write(name[:-4] + "\n")
    begin = time.time()

    all_matches = []
    for feature_set in database:
        feature_set_destination = feature_set[0]
        all_matches.append(bfm.knnMatch(destination, feature_set_destination, k = 2))

        all_good = []
        all_length = []

        for matches in all_matches:
            good = []
            for m,n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append([m])
            all_good.append(good)
            all_length.append(len(good))

    biggest_index, _ = feat.index_of_biggest(all_length)
    total_time = time.time() - begin
    txt.write("origin name : " + database[biggest_index][1][:-4] + "\n")
    txt.write("origin match: " + str(all_length[biggest_index]) + "\n")
    txt.write("--- %.2f sec ---" % total_time + "\n")
    txt.write("\n")
    txt.close()
    return total_time

def exp(datatype, feature, filename):
    image_names = glob.glob("temp\\match\\" + datatype + "\\r\\*.png")
    time = 0
    for image_name in image_names:
        image_name = image_name[14 + len(datatype):]
        time = time + croppedImageMatchFeatureDatabase(image_name, datatype, feature, filename)
    time = time / len(image_names)
    txt = open(filename + ".txt", "a")
    txt.write("average tiem = %.2f sec" % time)
    txt.close()

def plot_NMR():
    x = ["Crop 4", "Crop Center", "Scaling"]
    xp = np.arange(len(x))
    y1 = [51 / 56 * 100, 40 / 56 * 100, 32 / 56 * 100]
    y2 = [44 / 45 * 100, 33 / 45 * 100, 23 / 45 * 100]
    plt.title("Image Recognition Rate with Different Method")
    plt.xlabel("Methods")
    plt.ylabel("Image Recognition Rate (%)")
    width = 0.4
    plt.bar([i - width / 2 for i in xp], y1, width=width, label = "User A", hatch = "...", color = "#FFFFFF", edgecolor = "C1")
    plt.bar([i + width / 2 for i in xp], y2, width=width, label = "User B", hatch = "////", color = "#FFFFFF", edgecolor = "C2")
    plt.xticks(xp, x)
    axes = plt.gca()
    axes.set_ylim([0, 100])
    plt.legend()
    plt.show()

if __name__ == "__main__":
    plot_NMR()