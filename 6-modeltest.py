import numpy as np
from PIL import Image
import joblib
import os

target_path = './image/'
source_result = []
for title in os.listdir(target_path):
    source_result.append(title.replace('.jpg', ''))


def predict(model):
    predict_result = []
    for q in range(100):
        pre_list = []

        for i in range(4):
            part_path = './segment/'+str(q)+'_'+str(i)+'.jpg'
            pix = np.asarray(Image.open(os.path.join(part_path)).resize((20, 40), Image.BILINEAR))
            pix = pix.reshape(20*40)
            pre_list.append(pix)

        pre_list = np.asarray(pre_list)
        result_list = model.predict(pre_list)
        print(result_list, q)

        predict_result.append(str(result_list[0]+result_list[1]+result_list[2]+result_list[3]))

    return predict_result


model = joblib.load('trained.model')
predict_result = predict(model)
print(source_result)
print(predict_result)
