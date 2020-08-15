from cv2 import cv2 as cv
from PIL import Image
from PIL import ImageFile
import pickle
import random

def index_of_biggest(array):
    biggest_index = 0
    second_biggest_index = -1

    for index in range(0, len(array)):
        if array[index] > array[biggest_index]:
            second_biggest_index = biggest_index
            biggest_index = index
    return biggest_index, second_biggest_index

def show_all_feature():
    try:
        feature_database = pickle.load(open("feature_database.p", "rb"))
        for feature_set in feature_database:
            print(feature_set[1] + ", " + feature_set[2] + ", " + feature_set[3])
    except (OSError, IOError):
        print("NO FEATURE DATABASE EXISTS")

def reindex_feature():
    feature_database = pickle.load(open("feature_database.p", "rb"))
    new_feature_database = []

    for xIndex in range(0, 2):
        for yIndex in range(0, 75):
            for feature_set in feature_database:
                name = str(xIndex) + "n" + str(yIndex)
                if feature_set[1] == name:
                    new_feature_database.append(feature_set)
                    break

    for new_feature_set in new_feature_database:
        print(new_feature_set[1] + ", " + new_feature_set[2] + ", " + new_feature_set[3])

    pickle.dump(feature_database, open("old_feature_database.p", "wb"))
    pickle.dump(new_feature_database, open("feature_database.p", "wb"))

def restore_index():
    try:
        feature_database = pickle.load(open("feature_database.p", "rb"))
        return len(feature_database)
    except (OSError, IOError):
        return 0

def restore_feature():
    try:
        feature_database = pickle.load(open("feature_database.p", "rb"))
        feature_position = "RESTORE"
        for feature in feature_database:
            feature_position += feature[1] + "," + feature[2] + "," + feature[3] + ";"
        feature_position += "RESTORE"
        return feature_position
    except (OSError, IOError):
        print("NO FEATURE DATABASE EXISTS")
        return "RESTORERESTORE"

def delete_feature(name):
    try:
        database = pickle.load(open("feature_database.p", "rb"))
        new_database = []

        for feature_set in database:
            if feature_set[1] != name:
                # print(feature_set[1])
                new_database.append(feature_set)

        pickle.dump(new_database, open("feature_database.p", "wb"))
    except (OSError, IOError):
        print("There is no Feature Database, so the Deleting Process has been canceled.")

def modify_feature_x_y(name, x, y):
    try:
        feature_database = pickle.load(open("feature_database.p", "rb"))

        for feature_set in feature_database:
            if feature_set[1] == name:
                feature_set[2] = x
                feature_set[3] = y

        pickle.dump(feature_database, open("feature_database.p", "wb"))
    except (OSError, IOError):
        print("There is no Feature Database, so the Deleting Process has be canceled.")

def save_image(byteArray, filename):
    with open(filename, "wb") as imageFile:
        imageFile.write(byteArray)
    image = Image.open(filename)
    image.save(filename)

def store_feature(byteArray, name, x, y, a):
    try:
        feature_database = pickle.load(open("feature_database.p", "rb"))

        for feature_set in feature_database:
            if feature_set[1] == name:
                print("NAMEEXISTED")
                return "STORENAMEEXISTEDSTORE"
    
        filename = "temp\\store\\original\\" + name + ".png"
        save_image(byteArray, filename)
    
        orb = cv.ORB_create(2000)
        image = cv.imread(filename, cv.IMREAD_GRAYSCALE)

        variance = cv.Laplacian(image, cv.CV_64F).var()
        if variance < 100:
            print(variance)
            print("BLURRY")
            return "STOREBLURRYSTORE"

        _, destination = orb.detectAndCompute(image, None)

        feature_set = []
        feature_set.append(destination)
        feature_set.append(name)
        feature_set.append(x)
        feature_set.append(y)

        feature_database.append(feature_set)
        pickle.dump(feature_database, open("feature_database.p", "wb"))
    except (OSError, IOError):
        filename = "temp\\store\\original\\" + name + ".png"
        save_image(byteArray, filename)

        orb = cv.ORB_create(2000)
        image = cv.imread(filename, cv.IMREAD_GRAYSCALE)

        variance = cv.Laplacian(image, cv.CV_64F).var()
        if variance < 200:
            print(variance)
            print("BLURRY")
            return "STOREBLURRYSTORE"

        _, destination = orb.detectAndCompute(image, None)

        feature_set = []
        feature_set.append(destination)
        feature_set.append(name)
        feature_set.append(x)
        feature_set.append(y)

        feature_database = []
        feature_database.append(feature_set)
        pickle.dump(feature_database, open("feature_database.p", "wb"))
    return "STORESUCCESSSTORE"

def match_feature(byteArray, a):
    ImageFile.LOAD_TRUNCATED_IMAGES = True

    filename = "temp\\match\\original\\" + str(100000+ random.randint(0, 99999)) + ".png"
    save_image(byteArray, filename)

    orb = cv.ORB_create(2000)
    bfm = cv.BFMatcher()
    image = cv.imread(filename, cv.IMREAD_GRAYSCALE)
    variance = cv.Laplacian(image, cv.CV_64F).var()
    if variance < 100:
        print(variance)
        print("BLURRY")
        return "MATCHBLURRYMATCH"
    _, destination = orb.detectAndCompute(image, None)

    try:
        feature_database = pickle.load(open("feature_database.p", "rb"))
        all_matches = []
        for feature_set in feature_database:
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

        biggest_index, _ = index_of_biggest(all_length)
        print("Index = " + str(biggest_index))
        print("Match = " + str(all_length[biggest_index]))
        print("Name = " + feature_database[biggest_index][1])
        print("X = " + feature_database[biggest_index][2])
        print("Y = " + feature_database[biggest_index][3])
        matched_position = "MATCH" + feature_database[biggest_index][1] + "," + feature_database[biggest_index][2] + "," + feature_database[biggest_index][3] + ";MATCH"
        print(matched_position)
        return matched_position
    except (OSError, IOError):
        print("There is no Feature Database, so the Matching Process has be canceled.")
        return "MATCHMATCH"