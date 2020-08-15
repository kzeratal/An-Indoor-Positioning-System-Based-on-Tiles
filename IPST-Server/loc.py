from cv2 import cv2 as cv
from PIL import Image
from PIL import ImageFile
from matplotlib import pyplot as plt
import numpy as np
import pickle
import os
import random
import time
import threading
import glob
import feat

def highest_feature(array):
    highest = 0
    for features in array:
        if features > highest:
            highest = features
    return highest

def matc0(byteArray, a):
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    filename = "exp\\0\\" + str(100000+ random.randint(0, 99999)) + ".png"
    feat.save_image(byteArray, filename)
    image = cv.imread(filename, cv.IMREAD_GRAYSCALE)
    variance = cv.Laplacian(image, cv.CV_64F).var()
    if a >= 45 and variance >= 200:
        filename = "exp\\1\\" + str(100000+ random.randint(0, 99999)) + ".png"
        feat.save_image(byteArray, filename)

def matc2(byteArray):
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    filename = "exp\\2\\" + str(100000+ random.randint(0, 99999)) + ".png"
    feat.save_image(byteArray, filename)

def match_local(name1, name2):
    orb = cv.ORB_create(1000)
    bfm = cv.BFMatcher()

    image0 = cv.imread("pre\\a\\" + name1, cv.IMREAD_GRAYSCALE)
    image1 = cv.imread("pre\\a\\" + name2, cv.IMREAD_GRAYSCALE)

    _, destination0 = orb.detectAndCompute(image0, None)
    _, destination1 = orb.detectAndCompute(image1, None)

    database = pickle.load(open("database\\store\\original_database.p", "rb"))
    
    all_matches0 = []
    all_matches1 = []
    all_length0 = []
    all_length1 = []

    for feature_set in database:
        feature_set_destination = feature_set[0]
        all_matches0.append(bfm.knnMatch(destination0, feature_set_destination, k = 2))

        all_good = []
        all_length0 = []

        for matches in all_matches0:
            good = []
            for m,n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append([m])
            all_good.append(good)
            all_length0.append(len(good))
    print("done")

    for feature_set in database:
        feature_set_destination = feature_set[0]
        all_matches1.append(bfm.knnMatch(destination1, feature_set_destination, k = 2))

        all_good = []
        all_length1 = []

        for matches in all_matches1:
            good = []
            for m,n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append([m])
            all_good.append(good)
            all_length1.append(len(good))
    print("done")

    len0 = np.array(all_length0)
    len1 = np.array(all_length1)

    biggest_index, _ = feat.index_of_biggest(len0)
    print(database[biggest_index][1])
    biggest_index, _ = feat.index_of_biggest(len1)
    print(database[biggest_index][1])
    # Red = ED1C24, 960C13
    # Blue = 1A61A8
    # Purple = C882C8, 800080
    plt.title("Tile #79 Difference of Orientation = 0°")
    plt.xlabel("Index of Image")
    plt.ylabel("Matched Features")
    plt.plot(len0, label = "Tile #79") #ED1C24 #00A2E8 #FF7F27
    axes = plt.gca()
    axes.set_ylim([0, 120])
    plt.legend()
    plt.show()

    plt.title("Tile #79 Difference of Orientation = 45°")
    plt.xlabel("Index of Image")
    plt.ylabel("Matched Features")
    plt.plot(len1, label = "Tile #79") #FF7F27 #800080 #C882C8
    axes = plt.gca()
    axes.set_ylim([0, 120])
    plt.legend()
    plt.show()

def match_database_itself():
    bfm = cv.BFMatcher()
    database1 = pickle.load(open("database\\store\\original_database.p", "rb"))
    database2 = database1
    result = []

    for feature_set1 in database1:
        all_matches0 = []
        name1 = feature_set1[1]
        print(name1)
        begin = time.time()
        destination1 = feature_set1[0]
        for feature_set2 in database2:
            name2 = feature_set2[1]
            destination2 = feature_set2[0]
            if name1 != name2:
                all_matches0.append(bfm.knnMatch(destination1, destination2, k = 2))

                all_good = []
                all_length0 = []

                for matches in all_matches0:
                    good = []
                    for m,n in matches:
                        if m.distance < 0.75 * n.distance:
                            good.append([m])
                    all_good.append(good)
                    all_length0.append(len(good))

        total_time = time.time() - begin
        len0 = np.array(all_length0)
        highest = highest_feature(len0)
        result.append(highest)
        print(result)
        print("%.2f" % total_time)
    plt.title("Uniqueness of Feature Database")
    plt.xlabel("Index of Image")
    plt.ylabel("Matched Features")
    plt.plot(result, label = "Highest Matched Features") #FF7F27 #800080 #C882C8
    axes = plt.gca()
    axes.set_ylim([0, 100])
    plt.legend()
    plt.show()

def match_time(name, database_type, feature):
    orb = cv.ORB_create(feature)
    bfm = cv.BFMatcher()

    image = cv.imread("temp\\match\\" + database_type + "\\" + name, cv.IMREAD_GRAYSCALE)
    _, destination = orb.detectAndCompute(image, None)
    database = pickle.load(open("database\\store\\" + database_type + "_database.p", "rb"))
    
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
    print("origin name : " + database[biggest_index][1])
    print("origin match: " + str(all_length[biggest_index]))
    print("--- %.2f sec ---" % total_time)
    print("")

def match_time0(name, database_type, feature, filename):
    orb = cv.ORB_create(feature)
    bfm = cv.BFMatcher()

    image = cv.imread("temp\\match\\" + database_type + "\\" + name, cv.IMREAD_GRAYSCALE)
    _, destination = orb.detectAndCompute(image, None)
    database = pickle.load(open("database\\store\\" + database_type + "_database.p", "rb"))

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

def indexes_higher_than_threshold(array, threshold):
    indexes = []
    for index in range(0, len(array)):
        if array[index] > threshold:
            indexes.append(index)
    return indexes

def indexes_higher_than_threshold_cadidate(array, candidate, threshold):
    indexes = []
    for index in range(0, len(array)):
        if array[index] > threshold:
            indexes.append(candidate[index])
    return indexes

def find_biggest_with_candidate(array, candidate):
    biggest_index = 0
    for index in range(0, len(candidate)):
        if array[biggest_index] < array[candidate[index]]:
            biggest_index = candidate[index]
    return biggest_index

def match_threshold(destination, database, threshold):
    bfm = cv.BFMatcher()
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
    return all_length

def match_threshold_candidate(destination, database, candidate, threshold):
    bfm = cv.BFMatcher()
    all_matches = []
    for index in candidate:
        feature_set_destination = database[index][0]
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
    return all_length

def crop_match(name, database_type, threshold, feature, filename):
    txt = open(filename + ".txt", "a")
    txt.write(name[:-4] + "\n")

    orb = cv.ORB_create(feature)
    image = []
    destinations = []
    database = []
    for index in range(1, 5):
        image.append(cv.imread("temp\\match\\" + database_type + "\\" + str(index) + "\\" + name, cv.IMREAD_GRAYSCALE))
        _, destination = orb.detectAndCompute(image[index - 1], None)
        destinations.append(destination)
        database.append(pickle.load(open("database\\store\\" + str(index) + "\\" + database_type + "_database.p", "rb")))

    begin = time.time()
    try:
        # First match
        base_result = match_threshold(destinations[0], database[0], threshold)
        candidate = indexes_higher_than_threshold(base_result, threshold)
        #print(candidate)
        
        # Second match
        result = match_threshold_candidate(destinations[1], database[1], candidate, threshold)
        for index in range(0, len(result)):
            base_result[candidate[index]] = base_result[candidate[index]] + result[index]
        candidate = indexes_higher_than_threshold(base_result, threshold * 2)
        #print(candidate)
        
        # Third match
        result = match_threshold_candidate(destinations[2], database[2], candidate, threshold)
        for index in range(0, len(result)):
            base_result[candidate[index]] = base_result[candidate[index]] + result[index]
        candidate = indexes_higher_than_threshold(base_result, threshold * 3)
        #print(candidate)
        
        # Forth match
        result = match_threshold_candidate(destinations[3], database[3], candidate, threshold)
        for index in range(0, len(result)):
            base_result[candidate[index]] = base_result[candidate[index]] + result[index]
        candidate = indexes_higher_than_threshold(base_result, threshold * 4)
        #print(candidate)

        winner = find_biggest_with_candidate(base_result, candidate)
        total_time = time.time() - begin
        txt.write("origin name : " + database[0][winner][1][:-4] + "\n")
        txt.write("origin match: " + str(base_result[winner]) + "\n")
        txt.write("--- %.2f sec ---" % total_time + "\n")
        txt.write("\n")
        return total_time
    except (UnboundLocalError, IndexError):
        total_time = time.time() - begin
        txt.write("Matching Failed" + "\n")
        txt.write("\n")
        txt.write("--- %.2f sec ---" % total_time + "\n")
        txt.write("\n")
        return total_time

def exp01(datatype, feature, filename):
    image_names = glob.glob("temp\\match\\" + datatype + "\\*.png")
    time = 0
    for image_name in image_names:
        image_name = image_name[12 + len(datatype):]
        time = time + match_time0(image_name, datatype, feature, filename)
    time = time / len(image_names)
    txt = open(filename + ".txt", "a")
    txt.write("average tiem = %.2f sec" % time)
    txt.close()

def exp01c(datatype, threshold, feature, filename):
    image_names = glob.glob("temp\\match\\" + datatype + "\\*.png")
    time = 0
    for image_name in image_names:
        image_name = image_name[12 + len(datatype):]
        time = time + crop_match(image_name, datatype, threshold, feature, filename)
    time = time / len(image_names)
    txt = open(filename + ".txt", "a")
    txt.write("average tiem = %.2f sec" % time)
    txt.close()