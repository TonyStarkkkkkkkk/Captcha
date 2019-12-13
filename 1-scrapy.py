import requests  # http客户端
import os  # 创建文件夹

os.makedirs('./image/', exist_ok=True)
IMAGE_URL = "http://zhjw.scu.edu.cn/img/captcha.jpg"


def request_download(name):
    r = requests.get(IMAGE_URL)
    with open('./image/' + str(name) + '.jpg', 'wb') as f:
        f.write(r.content)


try:
    for i in range(200):
        request_download(i)
    print("finished")
except Exception as e:
    print(e)
