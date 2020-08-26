from cv2 import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
import glob
import os

def smooth(image, size):
    return cv.GaussianBlur(image, (size, size), 0)

def cropToFivePieces(image):
    width = image.shape[1]
    height = image.shape[0]
    image1 = image[0 : int(width / 2), 0 : int(height / 2)]
    image2 = image[0 : int(width / 2), int(height / 2) : height]
    image3 = image[int(width / 2) : width, 0 : int(height / 2)]
    image4 = image[int(width / 2) : width, int(height / 2) : height]
    image5 = image[int(width / 4) : int(width * 3 / 4), int(height / 4) : int(height * 3 / 4)]
    return image1, image2, image3, image4, image5

def doesCroppedImageExist(lastname, directory):
    if os.path.exists(directory + "\\1\\" + lastname):
        if os.path.exists(directory + "\\2\\" + lastname):
            if os.path.exists(directory + "\\3\\" + lastname):
                if os.path.exists(directory + "\\4\\" + lastname):
                    if os.path.exists(directory + "\\5\\" + lastname):
                        if os.path.exists(directory + "\\r\\" + lastname):
                            return True
    return False

def process_image(image, method, size):
    if method == "original":
        return image
    if method == "smooth":
        return smooth(image, size)

def preprocess(method, size):
    if method != "smooth" and method != "original":
        print("no method found")
        return

    # store
    names = glob.glob("temp\\store\\original\\*.png")
    directory = None

    if size is None:
        directory = "temp\\store\\" + method
    else:
        directory = "temp\\store\\" + method + str(size)
    if not os.path.exists(directory):
        os.makedirs(directory)

    for index in range(1, 6):
        if not os.path.exists(directory + "\\" + str(index)):
            os.makedirs(directory + "\\" + str(index))
        
    for name in names:
        lastname = name[name.rfind("\\") + 1:]
        image = None
        if not os.path.exists(directory + "\\" + lastname):
            image = cv.imread(name)
            image = process_image(image, method, size)
            cv.imwrite(directory + "\\" + lastname, image)
        if not doesCroppedImageExist(lastname, directory):
            if image is None:
                image = cv.imread(name)
                image = process_image(image, method, size)
            resized_image = cv.resize(image, (500, 500))
            image1, image2, image3, image4, image5 = cropToFivePieces(image)
            cv.imwrite(directory + "\\1\\" + lastname, image1)
            cv.imwrite(directory + "\\2\\" + lastname, image2)
            cv.imwrite(directory + "\\3\\" + lastname, image3)
            cv.imwrite(directory + "\\4\\" + lastname, image4)
            cv.imwrite(directory + "\\5\\" + lastname, image5)
            cv.imwrite(directory + "\\r\\" + lastname, resized_image)

    # match
    names = glob.glob("temp\\match\\original\\*.png")
    directory = None

    if size is None:
        directory = "temp\\match\\" + method
    else:
        directory = "temp\\match\\" + method + str(size)
    if not os.path.exists(directory):
        os.makedirs(directory)

    for index in range(1, 6):
        if not os.path.exists(directory + "\\" + str(index)):
            os.makedirs(directory + "\\" + str(index))

    for name in names:
        lastname = name[name.rfind("\\") + 1:]
        image = None
        if not os.path.exists(directory + "\\" + lastname):
            image = cv.imread(name)
            image = process_image(image, method, size)
            cv.imwrite(directory + "\\" + lastname, image)
        if not doesCroppedImageExist(lastname, directory):
            if image is None:
                image = cv.imread(name)
                image = process_image(image, method, size)
            resized_image = cv.resize(image, (500, 500))
            image1, image2, image3, image4, image5 = cropToFivePieces(image)
            cv.imwrite(directory + "\\1\\" + lastname, image1)
            cv.imwrite(directory + "\\2\\" + lastname, image2)
            cv.imwrite(directory + "\\3\\" + lastname, image3)
            cv.imwrite(directory + "\\4\\" + lastname, image4)
            cv.imwrite(directory + "\\5\\" + lastname, image5)
            cv.imwrite(directory + "\\r\\" + lastname, resized_image)

if __name__ == "__main__":
    #preprocess("original", None)
    preprocess("smooth", 9)