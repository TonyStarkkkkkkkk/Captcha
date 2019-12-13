import numpy as np
import os
from PIL import Image
import joblib
from sklearn.neighbors import KNeighborsClassifier


def load_dataset():
    X = []
    y = []
    for i in '2345678ABCDEFGMNPWXY':
        target_path = './classify/' + i
        for title in os.listdir(target_path):
            pix = np.asarray(Image.open(os.path.join(target_path, title)).resize((20, 40), Image.BILINEAR))
            X.append(pix.reshape(20*40))
            y.append(target_path.split('/')[-1])

    X = np.asarray(X)

    y = np.asarray(y)
    return X, y


def check_everyone(model):
    pre_list = []
    y_list = []
    for i in '2345678ABCDEFGMNPWXY':
        part_path = "./classify/"+i
        for title in os.listdir(part_path):
            pix = np.asarray(Image.open(os.path.join(part_path, title)).resize((20, 40), Image.BILINEAR))
            pix = pix.reshape(20*40)
            pre_list.append(pix)
            y_list.append(part_path.split('/')[-1])
    pre_list = np.asarray(pre_list)
    y_list = np.asarray(y_list)
    result_list = model.predict(pre_list)
    acc = 0
    for i in range(len(result_list)):
        if result_list[i] == y_list[i]:
            acc += 1
    print(acc, acc/len(result_list))


X, y = load_dataset()
knn = KNeighborsClassifier()
knn.fit(X, y)
joblib.dump(knn, 'trained.model')
check_everyone(knn)
