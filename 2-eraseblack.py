import os
from PIL import Image, ImageDraw

os.makedirs('./eraseBlack/', exist_ok=True)


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


for i in range(200):
    path = './image/' + str(i) + '.jpg'
    image = Image.open(path)
    ave = getAve(image)
    path1 = "./eraseBlack/" + str(i) + ".jpg"
    saveImage(image, path1, image.size, ave)
print('finished')