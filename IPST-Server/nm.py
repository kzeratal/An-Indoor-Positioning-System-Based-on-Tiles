from cv2 import cv2 as cv
import glob

names = glob.glob("temp\\store\\original\\*.png")
for name in names:
    print(name)