from cv2 import cv2 as cv
from tileLoc import index_of_biggest
from matplotlib import pyplot as plt
import numpy as np
import glob
import pickle

def top_two_of_array(array):
    top1 = 0
    top2 = -1

    for index in range(0, len(array)):
        if array[index] > array[top1]:
            top2 = top1
            top1 = index
    return top1, top2

def show_store_database(name):
    try:
        database = pickle.load(open("database\\store\\" + name + "_database.p", "rb"))
        for feature_set in database:
            print(feature_set[1] + ", " + str(feature_set[2]))
            print(len(feature_set[0]))
    except (OSError, IOError):
        print("Database doesn't exist")

def show_store_crop_database(name):
    try:
        for index in range(1, 5):
            database = pickle.load(open("database\\store\\" + str(index) + "\\" + name + "_database.p", "rb"))
            for feature_set in database:
                print(feature_set[1] + ", " + str(feature_set[2]))
                print(len(feature_set[0]))
    except (OSError, IOError):
        print("Database doesn't exist")

def show_match_database(name):
    try:
        database = pickle.load(open("database\\match\\" + name + "_database.p", "rb"))
        for feature_set in database:
            print(feature_set[1] + ", " + str(feature_set[2]))
    except (OSError, IOError):
        print("Database doesn't exist")

def create_crop_database(database_type, feature):
    orb = cv.ORB_create(feature)

    for index in range(1, 5):
        image_names = glob.glob("temp\\store\\" + database_type + "\\" + str(index) + "\\" + "*.png")
        database = [] 
        for image_name in image_names:
            image = cv.imread(image_name, cv.IMREAD_GRAYSCALE)
            variance = cv.Laplacian(image, cv.CV_64F).var()
            _, destination = orb.detectAndCompute(image, None)
            lastname = image_name[image_name.rfind("\\") + 1:]
            feature_set = []
            feature_set.append(destination)
            feature_set.append(lastname)
            feature_set.append(variance)
            database.append(feature_set)
        pickle.dump(database, open("database\\store\\" + str(index) + "\\" + database_type + "_database.p", "wb"))

        image_names = glob.glob("temp\\match\\" + database_type + "\\" + str(index) + "\\" + "*.png")
        database = [] 
        for image_name in image_names:
            image = cv.imread(image_name, cv.IMREAD_GRAYSCALE)
            variance = cv.Laplacian(image, cv.CV_64F).var()
            _, destination = orb.detectAndCompute(image, None)
            lastname = image_name[image_name.rfind("\\") + 1:]
            feature_set = []
            feature_set.append(destination)
            feature_set.append(lastname)
            feature_set.append(variance)
            database.append(feature_set)
        pickle.dump(database, open("database\\match\\" + str(index) + "\\" + database_type + "_database.p", "wb"))

def create_database(database_type, feature):
    orb = cv.ORB_create(feature)

    image_names = glob.glob("temp\\store\\" + database_type + "\\*.png")
    database = [] 
    for image_name in image_names:
        image = cv.imread(image_name, cv.IMREAD_GRAYSCALE)
        variance = cv.Laplacian(image, cv.CV_64F).var()
        _, destination = orb.detectAndCompute(image, None)
        lastname = image_name[image_name.rfind("\\") + 1:]
        feature_set = []
        feature_set.append(destination)
        feature_set.append(lastname)
        feature_set.append(variance)
        database.append(feature_set)
    pickle.dump(database, open("database\\store\\" + database_type + "_database.p", "wb"))

    image_names = glob.glob("temp\\match\\" + database_type + "\\*.png")
    database = [] 
    for image_name in image_names:
        image = cv.imread(image_name, cv.IMREAD_GRAYSCALE)
        variance = cv.Laplacian(image, cv.CV_64F).var()
        _, destination = orb.detectAndCompute(image, None)
        lastname = image_name[image_name.rfind("\\") + 1:]
        feature_set = []
        feature_set.append(destination)
        feature_set.append(lastname)
        feature_set.append(variance)
        database.append(feature_set)
    pickle.dump(database, open("database\\match\\" + database_type + "_database.p", "wb"))

def create_store_info(name):
    bfm = cv.BFMatcher()

    match_database = pickle.load(open("database\\store\\" + name + "_database.p", "rb"))
    store_database = pickle.load(open("database\\store\\" + name + "_database.p", "rb"))

    match_filename_results = []
    match_top1_index_results = []
    match_top1_amount_results = []
    match_top2_amount_results = []
    match_diff_results = []

    for match_feature_set in match_database:
        match_feature_set_destination = match_feature_set[0]
        all_good = [] # 一張圖與資料庫所有圖的比對個數

        for store_feature_set in store_database:
            if store_feature_set[1] != match_feature_set[1]:
                store_feature_set_destination = store_feature_set[0]
                matches = bfm.knnMatch(match_feature_set_destination, store_feature_set_destination, k = 2)
                good = [] # 一張圖與資料庫另一張圖的比對個數

                for m, n in matches:
                    if m.distance < 0.75 * n.distance:
                        good.append([m])
                all_good.append(len(good))
        
        # 某圖已經與資料庫中所有圖比對完畢
        index_top1, index_top2 = top_two_of_array(all_good)
        match_top1_amount = all_good[index_top1]
        match_top2_amount = all_good[index_top2]
        match_diff = match_top1_amount - match_top2_amount

        match_filename_results.append(store_database[index_top1][1])
        match_top1_index_results.append(index_top1)
        match_top1_amount_results.append(match_top1_amount)
        match_top2_amount_results.append(match_top2_amount)
        match_diff_results.append(match_diff)
        print(match_feature_set[1] + " Done!")

    match_info = []
    match_info.append(match_filename_results)
    match_info.append(match_top1_index_results)
    match_info.append(match_top1_amount_results)
    match_info.append(match_top2_amount_results)
    match_info.append(match_diff_results)

    pickle.dump(match_info, open("database\\store\\" + name + "_match_info.p", "wb"))

def create_crop_match_info(name):
    bfm = cv.BFMatcher()

    for index in range(1, 5):
        match_database = pickle.load(open("database\\match\\" + str(index) + "\\" + name + "_database.p", "rb"))
        store_database = pickle.load(open("database\\store\\" + str(index) + "\\" + name + "_database.p", "rb"))

        match_filename_results = []
        match_top1_index_results = []
        match_top1_amount_results = []
        match_top2_amount_results = []
        match_diff_results = []

        for match_feature_set in match_database:
            match_feature_set_destination = match_feature_set[0]
            all_good = [] # 一張圖與資料庫所有圖的比對個數

            for store_feature_set in store_database:
                store_feature_set_destination = store_feature_set[0]
                matches = bfm.knnMatch(match_feature_set_destination, store_feature_set_destination, k = 2)
                good = [] # 一張圖與資料庫另一張圖的比對個數

                for m, n in matches:
                    if m.distance < 0.75 * n.distance:
                        good.append([m])
                all_good.append(len(good))
            
            # 某圖已經與資料庫中所有圖比對完畢
            index_top1, index_top2 = top_two_of_array(all_good)
            match_top1_amount = all_good[index_top1]
            match_top2_amount = all_good[index_top2]
            match_diff = match_top1_amount - match_top2_amount

            match_filename_results.append(store_database[index_top1][1])
            match_top1_index_results.append(index_top1)
            match_top1_amount_results.append(match_top1_amount)
            match_top2_amount_results.append(match_top2_amount)
            match_diff_results.append(match_diff)
            print(match_feature_set[1] + " Done!")

        match_info = []
        match_info.append(match_filename_results)
        match_info.append(match_top1_index_results)
        match_info.append(match_top1_amount_results)
        match_info.append(match_top2_amount_results)
        match_info.append(match_diff_results)

        pickle.dump(match_info, open("database\\match\\" + str(index) + "\\" + name + "_match_info.p", "wb"))

def create_match_info(name):
    bfm = cv.BFMatcher()

    match_database = pickle.load(open("database\\match\\" + name + "_database.p", "rb"))
    store_database = pickle.load(open("database\\store\\" + name + "_database.p", "rb"))

    match_filename_results = []
    match_top1_index_results = []
    match_top1_amount_results = []
    match_top2_amount_results = []
    match_diff_results = []

    for match_feature_set in match_database:
        match_feature_set_destination = match_feature_set[0]
        all_good = [] # 一張圖與資料庫所有圖的比對個數

        for store_feature_set in store_database:
            store_feature_set_destination = store_feature_set[0]
            matches = bfm.knnMatch(match_feature_set_destination, store_feature_set_destination, k = 2)
            good = [] # 一張圖與資料庫另一張圖的比對個數

            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append([m])
            all_good.append(len(good))
        
        # 某圖已經與資料庫中所有圖比對完畢
        index_top1, index_top2 = top_two_of_array(all_good)
        match_top1_amount = all_good[index_top1]
        match_top2_amount = all_good[index_top2]
        match_diff = match_top1_amount - match_top2_amount

        match_filename_results.append(store_database[index_top1][1])
        match_top1_index_results.append(index_top1)
        match_top1_amount_results.append(match_top1_amount)
        match_top2_amount_results.append(match_top2_amount)
        match_diff_results.append(match_diff)
        print(match_feature_set[1] + " Done!")

    match_info = []
    match_info.append(match_filename_results)
    match_info.append(match_top1_index_results)
    match_info.append(match_top1_amount_results)
    match_info.append(match_top2_amount_results)
    match_info.append(match_diff_results)

    pickle.dump(match_info, open("database\\match\\" + name + "_match_info.p", "wb"))

def plot_ex11():
    plt.title("Effectiveness of Scale")
    plt.ylim(30, 105)
    plt.plot(["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%", "110%"], [30, 70, 100, 100, 100, 100, 100, 100, 100, 100, 100], label = "PN (%)")
    plt.xlabel("Scale of Original Width")
    plt.ylabel("PN")
    plt.legend()
    plt.show()

def plot_ex12():
    plt.title("Effectiveness of Scale")
    plt.ylim(30, 105)
    plt.plot(["120%", "130%", "140%", "150%", "160%", "170%", "180%", "190%", "200%", "210%", "220%"], [100, 100, 100, 100, 100, 100, 100, 100, 100, 90, 90], label = "PN (%)")
    plt.xlabel("Scale of Original Width")
    plt.ylabel("PN")
    plt.legend()
    plt.show()

def plot_store_info(name):
    match_info = pickle.load(open("database\\store\\" + name + "_match_info.p", "rb"))

    print(match_info[0])

    index = np.arange(0, len(match_info[0]))
    top1_amount = match_info[2]
    top2_amount = match_info[3]
    diff = match_info[4]

    plt.title(name[0].upper() + name[1:] + " Uniqueness")
    plt.xlabel("Index of Image in Database")
    plt.ylabel("Matched Features")
    plt.yticks(np.arange(0, 350, step = 50))
    plt.ylim(0, 300)
    plt.plot(index, top1_amount, label = "Highest")
    #plt.bar(index, top2_amount, label = "Second Highest", width = 0.2)
    #plt.bar(index + 0.2, diff, label = "Difference", width = 0.2)
    plt.legend()
    plt.show()

def plot_crop_match_info(name):
    top1_amount_sum = None
    top2_amount_sum = None
    diff_sum = None
    figure_index_sum = None

    for index in range(1, 5):
        match_info = pickle.load(open("database\\match\\" + str(index) + "\\" + name + "_match_info.p", "rb"))

        print(match_info[0])
        figure_index = np.arange(0, len(match_info[0]))
        top1_amount = match_info[2]
        top2_amount = match_info[3]
        diff = match_info[4]
        print(top1_amount)
        print(top2_amount)
        print(diff)
        if index == 1:
            figure_index_sum = figure_index
            top1_amount_sum = np.array(top1_amount)
            top2_amount_sum = np.array(top2_amount)
            diff_sum = np.array(diff)
        else:
            top1_amount_sum += np.array(top1_amount)
            top2_amount_sum += np.array(top2_amount)
            diff_sum += +np.array(diff)

        plt.title(name + ", " + str(index))
        plt.xlabel("Index of Image in Database")
        plt.ylabel("Matched Features")
        plt.xticks(figure_index)
        plt.bar(figure_index - 0.2, top1_amount, label = "Highest", width = 0.2)
        plt.bar(figure_index, top2_amount, label = "Second Highest", width = 0.2)
        plt.bar(figure_index + 0.2, diff, label = "Difference", width = 0.2)
        plt.legend()
        plt.show()
    
    print(top1_amount_sum)
    print(top2_amount_sum)
    print(diff_sum)
    plt.title(name + ", total")
    plt.xlabel("Index of Image in Database")
    plt.ylabel("Matched Features")
    plt.xticks(figure_index_sum)
    plt.bar(figure_index_sum - 0.2, top1_amount_sum, label = "Highest", width = 0.2)
    plt.bar(figure_index_sum, top2_amount_sum, label = "Second Highest", width = 0.2)
    plt.bar(figure_index_sum + 0.2, diff_sum, label = "Difference", width = 0.2)
    plt.legend()
    plt.show()

def plot_match_info(name):
    match_info = pickle.load(open("database\\match\\" + name + "_match_info.p", "rb"))

    print(match_info[0])

    index = np.arange(0, len(match_info[0]))
    top1_amount = match_info[2]
    top2_amount = match_info[3]
    diff = match_info[4]

    plt.title(name)
    plt.xlabel("Index of Image in Database")
    plt.ylabel("Matched Features")
    plt.xticks(index)
    plt.bar(index - 0.2, top1_amount, label = "Highest", width = 0.2)
    plt.bar(index, top2_amount, label = "Second Highest", width = 0.2)
    plt.bar(index + 0.2, diff, label = "Difference", width = 0.2)
    plt.legend()
    plt.show()

def plot_variance(name):
    store_database = pickle.load(open("database\\store\\" + name + "_database.p", "rb"))
    match_database = pickle.load(open("database\\match\\" + name + "_database.p", "rb"))
    match_info = pickle.load(open("database\\match\\" + name + "_match_info.p", "rb"))

    match_variance = []
    store_variance = []

    for feature_set in match_database:
        match_variance.append(feature_set[2])

    for name in match_info[0]:
        for feature_set in store_database:
            if feature_set[1] == name:
                store_variance.append(feature_set[2])

    match_variance_a = np.array(match_variance)
    store_variance_a = np.array(store_variance)
    match_info_a = np.array(match_info[2])

    print(match_variance_a)
    print(store_variance_a)
    print(match_info_a)

    bound = len(store_variance_a) - 1
    for index in range(len(store_variance_a)):
        print(match_info_a[bound - index])
        if store_variance_a[bound - index] > 700:
            match_variance_a = np.delete(match_variance_a, bound - index)
            store_variance_a = np.delete(store_variance_a, bound - index)
            match_info_a = np.delete(match_info_a, bound - index)

    plt.title("Variance")
    plt.xlabel("Index of Image been Matched")
    plt.plot(match_variance_a, label = "Match Variance")
    plt.plot(store_variance_a, label = "Database Variance")
    plt.plot(match_info_a, label = "Matched Features")
    plt.legend()
    plt.show()

def plot_all_match_info():
    names = glob.glob("database\\match\\*_match_info.p")

    top1_amount_means = []
    top2_amount_means = []
    diff_means = []

    for name in names:
        match_info = pickle.load(open(name, "rb"))

        top1_amount_array = np.array(match_info[2])
        top2_amount_array = np.array(match_info[3])
        diff_array = np.array(match_info[4])

        top1_amount_mean = round(top1_amount_array.mean(), 3)
        top2_amount_mean = round(top2_amount_array.mean(), 3)
        diff_mean = round(diff_array.mean(), 3)

        top1_amount_means.append(top1_amount_mean)
        top2_amount_means.append(top2_amount_mean)
        diff_means.append(diff_mean)

    plt.title("Mean of the Highest Feature")
    plt.xlabel("Method")
    plt.ylabel("Matched Features")

    for index in range(0, len(names)):
        print(names[index][15:-13], top1_amount_means[index], top2_amount_means[index], diff_means[index])
        plt.bar(names[index][15:-13], top1_amount_means[index], label = names[index][15:-13])

    plt.legend()
    plt.show()

    plt.title("Mean of the Second Highest Feature")
    plt.xlabel("Method")
    plt.ylabel("Matched Features")

    for index in range(0, len(names)):
        print(names[index][15:-13], top1_amount_means[index], top2_amount_means[index], diff_means[index])
        plt.bar(names[index][15:-13], top2_amount_means[index], label = names[index][15:-13])

    plt.legend()
    plt.show()

    plt.title("Mean of the Difference")
    plt.xlabel("Method")
    plt.ylabel("Matched Features")

    for index in range(0, len(names)):
        print(names[index][15:-13], top1_amount_means[index], top2_amount_means[index], diff_means[index])
        plt.bar(names[index][15:-13], diff_means[index], label = names[index][15:-13])

    plt.legend()
    plt.show()

def plot_match_database(name):
    bfm = cv.BFMatcher()

    match_database = pickle.load(open("database\\match\\" + name + "_database.p", "rb"))
    store_database = pickle.load(open("database\\store\\" + name + "_database.p", "rb"))

    for match_feature_set in match_database:
        match_feature_set_destination = match_feature_set[0]
        all_good = []
        for store_feature_set in store_database:
            store_feature_set_destination = store_feature_set[0]
            matches = bfm.knnMatch(match_feature_set_destination, store_feature_set_destination, k = 2)
            good = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append([m])
            all_good.append(len(good))
        all_good_array = np.array(all_good)
        x = np.arange(0, len(all_good_array))
        y = all_good_array[x]
        plt.title(name)
        plt.xlabel("index of image in database")
        plt.ylabel("matched feature")
        plt.plot(x, y)
        plt.show()

if __name__ == "__main__":
    # 1. use preprocess to generate images
    # 2. use create_database("database type") to generate database
    # 3. use create_match_info("database type") to generate match info
    # 4. use plot_match_info("database type") to sketch match info

    #create_database("original")
    #create_crop_database("original")
    create_database("smooth9", 500)
    #create_crop_database("smooth9", 300)