import cv2
import os
from matplotlib import pyplot as plt

os.makedirs('./shadow/', exist_ok=True)


def createShadow(img):
    GrayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh1 = cv2.threshold(GrayImage, 130, 255, cv2.THRESH_BINARY)
    (h, w, c) = img.shape

    a = [0 for z in range(w)]

    for j in range(w):
        for i in range(h):
            if thresh1[i, j] == 0:
                a[j] += 1
                thresh1[i, j] = 255

    for j in range(0, w):
        for i in range((h-a[j]), h):
            thresh1[i, j] = 0

    plt.imshow(thresh1, cmap=plt.gray())
    plt.show()
    return thresh1


for i in range(10):
    path = './denoise/'+str(i)+'.jpg'
    path1 = './shadow/'+str(i)+'.jpg'
    img = cv2.imread(path)
    cv2.imwrite(path1, createShadow(img))
