from cv2 import cv2 as cv
from matplotlib import pyplot as plt
import numpy as np
import glob
import os

def var():
    names = glob.glob("exp\\0\\*.png")
    for name in names:
        image = cv.imread(name)
        variance = cv.Laplacian(image, cv.CV_64F).var()
        print(variance)

def perspective15():
    image = cv.imread("pre\\a\\a15.png")
    src_points = np.array([[325., 765,], [365., 550.], [825., 550.], [875, 765.]], dtype = "float32")
    dst_points = np.array([[0., 1224.], [0., 0.], [1224., 0.], [1224., 1224.]], dtype = "float32")
    mat = cv.getPerspectiveTransform(src_points, dst_points)
    perspective = cv.warpPerspective(image, mat, (1224, 1224))
    cv.imwrite("pre\\a\\kc15.png", perspective)

def perspective30():
    image = cv.imread("pre\\a\\a30.png")
    src_points = np.array([[230., 820,], [305., 415.], [930., 415.], [1020, 820.]], dtype = "float32")
    dst_points = np.array([[0., 1224.], [0., 0.], [1224., 0.], [1224., 1224.]], dtype = "float32")
    mat = cv.getPerspectiveTransform(src_points, dst_points)
    perspective = cv.warpPerspective(image, mat, (1224, 1224))
    cv.imwrite("pre\\a\\kc30.png", perspective)

def perspective45():
    image = cv.imread("pre\\a\\a45.png")
    src_points = np.array([[80., 926,], [200., 240.], [1020., 240.], [1130, 926.]], dtype = "float32")
    dst_points = np.array([[0., 1224.], [0., 0.], [1224., 0.], [1224., 1224.]], dtype = "float32")
    mat = cv.getPerspectiveTransform(src_points, dst_points)
    perspective = cv.warpPerspective(image, mat, (1224, 1224))
    cv.imwrite("pre\\a\\kc45.png", perspective)


def smooth(image, size):
    return cv.GaussianBlur(image, (size, size), 0)

def crop(image):
    width = image.shape[1]
    height = image.shape[0]
    image1 = image[0 : int(width / 2), 0 : int(height / 2)]
    image2 = image[0 : int(width / 2), int(height / 2) : height]
    image3 = image[int(width / 2) : width, 0 : int(height / 2)]
    image4 = image[int(width / 2) : width, int(height / 2) : height]
    return image1, image2, image3, image4

def crop2(image):
    width = image.shape[1]
    height = image.shape[0]
    image1 = image[0 : int(width / 2), 0 : height]
    image2 = image[int(width / 2): width, 0  : height]
    return image1, image2

def doesCropExist(lastname, directory):
    if os.path.exists(directory + "\\1\\" + lastname):
        if os.path.exists(directory + "\\2\\" + lastname):
            if os.path.exists(directory + "\\3\\" + lastname):
                if os.path.exists(directory + "\\4\\" + lastname):
                    return True
    return False

def doesCropExist2(lastname, directory):
    if os.path.exists(directory + "\\1\\" + lastname):
        if os.path.exists(directory + "\\2\\" + lastname):
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

    for index in range(1, 5):
        if not os.path.exists(directory + "\\" + str(index)):
            os.makedirs(directory + "\\" + str(index))
        
    for name in names:
        lastname = name[name.rfind("\\") + 1:]
        image = None
        if not os.path.exists(directory + "\\" + lastname):
            image = cv.imread(name)
            image = process_image(image, method, size)
            cv.imwrite(directory + "\\" + lastname, image)
        if not doesCropExist(lastname, directory):
            if image is None:
                image = cv.imread(name)
                image = process_image(image, method, size)
            image1, image2, image3, image4 = crop(image)
            #image1, image2 = crop2(image)
            cv.imwrite(directory + "\\1\\" + lastname, image1)
            cv.imwrite(directory + "\\2\\" + lastname, image2)
            cv.imwrite(directory + "\\3\\" + lastname, image3)
            cv.imwrite(directory + "\\4\\" + lastname, image4)

    # match
    names = glob.glob("temp\\match\\original\\*.png")
    directory = None

    if size is None:
        directory = "temp\\match\\" + method
    else:
        directory = "temp\\match\\" + method + str(size)
    if not os.path.exists(directory):
        os.makedirs(directory)

    for index in range(1, 5):
        if not os.path.exists(directory + "\\" + str(index)):
            os.makedirs(directory + "\\" + str(index))

    for name in names:
        lastname = name[name.rfind("\\") + 1:]
        image = None
        if not os.path.exists(directory + "\\" + lastname):
            image = cv.imread(name)
            image = process_image(image, method, size)
            cv.imwrite(directory + "\\" + lastname, image)
        if not doesCropExist(lastname, directory):
            if image is None:
                image = cv.imread(name)
                image = process_image(image, method, size)
            image1, image2, image3, image4 = crop(image)
            cv.imwrite(directory + "\\1\\" + lastname, image1)
            cv.imwrite(directory + "\\2\\" + lastname, image2)
            cv.imwrite(directory + "\\3\\" + lastname, image3)
            cv.imwrite(directory + "\\4\\" + lastname, image4)

if __name__ == "__main__":
    preprocess("original", None)
    #preprocess("smooth", 9)