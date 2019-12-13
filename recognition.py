import os
import requests
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import joblib

IMAGE_URL = "http://zhjw.scu.edu.cn/img/captcha.jpg"
t2val = {}


def getAve(image):
    s, ave = 0, 0
    width = image.size[0]
    height = image.size[1]

    for x in range(width):
        for y in range(height):
            (r, g, b) = image.getpixel((x, y))
            s = s + r + g + b
    ave = s/width/height/3
    return ave


def saveImage(image, filename, size, ave):
    draw = ImageDraw.Draw(image)
    for x in range(size[0]):
        for y in range(size[1]):
            (r, g, b) = image.getpixel((x, y))
            ave2 = (int(r) + int(g) + int(b))/3
            if ave2 < ave-150 and abs(r - g) < 40:
                draw.point((x, y), (255, 255, 255))
    image.save(filename)


def twoValue(image, G):
    for y in range(image.size[1]):
        for x in range(image.size[0]):
            g = image.getpixel((x, y))
            if g > G:
                t2val[(x, y)] = 1
            else:
                t2val[(x, y)] = 0

        # 根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值N（0 <N <8），当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点
        # G: Integer 图像二值化阈值
        # N: Integer 降噪率 0 <N <8
        # Z: Integer 降噪次数
        # 输出
        #  0：降噪成功
        #  1：降噪失败


def clearNoise(image, N, Z):
    for i in range(Z):
        t2val[(0, 0)] = 1
        t2val[(image.size[0]-1, image.size[1]-1)] = 1

        for x in range(1, image.size[0] - 1):
            for y in range(1, image.size[1] - 1):
                nearDots = 0
                L = t2val[(x, y)]
                if L == t2val[(x - 1, y - 1)]:
                    nearDots += 1
                if L == t2val[(x - 1, y)]:
                    nearDots += 1
                if L == t2val[(x - 1, y + 1)]:
                    nearDots += 1
                if L == t2val[(x, y - 1)]:
                    nearDots += 1
                if L == t2val[(x, y + 1)]:
                    nearDots += 1
                if L == t2val[(x + 1, y - 1)]:
                    nearDots += 1
                if L == t2val[(x + 1, y)]:
                    nearDots += 1
                if L == t2val[(x + 1, y + 1)]:
                    nearDots += 1
                if nearDots < N:
                    t2val[(x, y)] = 1


def saveImage2(filename, size):
    image = Image.new("1", size)
    draw = ImageDraw.Draw(image)

    for x in range(size[0]):
        for y in range(size[1]):
            if (5 <= x <= size[0]-5) and (5 <= y <= size[1]-5):
                draw.point((x, y), t2val[(x, y)])
            else:
                draw.point((x, y), 1)   # 去边缘
    image.save(filename)


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


def predict(model):
    predict_result = []
    pre_list = []
    for i in range(4):
        part_path = 'test-4_'+str(i)+'.jpg'
        pix = np.asarray(Image.open(os.path.join(part_path)).resize((20, 40), Image.BILINEAR))
        pix = pix.reshape(20*40)
        pre_list.append(pix)

    pre_list = np.asarray(pre_list)
    result_list = model.predict(pre_list)
    # print(result_list)

    predict_result.append(str(result_list[0]+result_list[1]+result_list[2]+result_list[3]))

    return predict_result


if __name__ == '__main__':

    # # 1. 下载图片
    # r = requests.get(IMAGE_URL)
    # with open('test.jpg', 'wb') as f:
    #     f.write(r.content)

    # 2. 去除黑线条
    image = Image.open('test.jpg')
    ave = getAve(image)
    saveImage(image, 'test-2.jpg', image.size, ave)

    # 3. 二值化&去噪

    image = Image.open('test-2.jpg')
    image = image.convert('L')
    twoValue(image, 160)
    clearNoise(image, 3, 4)
    saveImage2('test-3.jpg', image.size)

    # 4. 图像分割

    img = Image.open('test-3.jpg')
    point = findEdge(img)
    for i in range(4):
        box = (point[1][i], point[0][0], point[1][i + 1], point[0][1])
        img.crop(box).save("test-4_" + str(i) + '.jpg')

    # 5. 识别

    model = joblib.load('trained.model')
    predict_result = predict(model)
    # print(predict_result)
    image = Image.open('test.jpg')
    plt.imshow(image)
    plt.show()
    # print(predict_result)
    print(''.join(predict_result))


