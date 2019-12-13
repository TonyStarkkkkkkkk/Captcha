import os
from PIL import Image

os.makedirs('./segment/', exist_ok=True)


def getCutPoint(lst, width):
    mid = len(lst)//2
    temp = lst[mid-width: mid+width+1]
    point = min(temp)
    return mid-width+temp.index(point)


def findEdge(img):
    hrz_begin, hrz_end = 0, 0
    ver_begin, ver_end = 0, 0
    w, h = img.size
    a = [0 for pw in range(w)]
    b = [0 for ph in range(h)]
    # 垂直投影
    for i in range(w):
        for j in range(h):
            if(img.getpixel((i, j))) <= 200:
                a[i] += 1

    for i in range(w):
        if a[i] >= 5:
            hrz_begin = i
            break
    for i in range(w-1, 0, -1):
        if a[i] >= 5:
            hrz_end = i
            break

    mid = getCutPoint(a[hrz_begin:hrz_end+1], 5)+hrz_begin
    mid_1 = getCutPoint(a[hrz_begin:mid+1], 3)+hrz_begin
    mid_2 = getCutPoint(a[mid: hrz_end+1], 3)+mid

    # 水平投影
    for j in range(h):
        for i in range(w):
            if(img.getpixel((i, j))) <= 200:
                b[j] += 1
    for i in range(h):
        if b[i] >= 5:
            ver_begin = i
            break
    for i in range(h-1, 0, -1):
        if b[i] >= 5:
            ver_end = i
            break
    return [(ver_begin, ver_end), (hrz_begin, mid_1, mid, mid_2, hrz_end)]


for ii in range(200):
    path = "./denoise/" + str(ii) + ".jpg"
    img = Image.open(path)
    outDir = "./segment/"
    point = findEdge(img)
    for i in range(len(point[1]) - 1):
        box = (point[1][i], point[0][0], point[1][i + 1], point[0][1])
        img.crop(box).save(outDir + str(400+ii) + "_" + str(i) + '.jpg')
print('finished')
