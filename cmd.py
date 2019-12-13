import http.cookiejar
import urllib.request
import re
import os
import random
import time
from sys import argv
import recognition

username = argv[1]
password = argv[2]


# 评教模块信息查询
def pjcx():

    pingyu = ["非常好",
              "nice",
              "good",
              "very good",
              "非常好",
              "老师很负责",
              "老师对同学和蔼可亲",
              "老师上课生动有趣",
              "老师的课让我学到了很多知识",
              "教学整体效果较好，课堂气氛也很活跃，在程度上也做了较好的拓展，使学生对所学内容有更深了解",
              "教师教学在书面浅显知识的基础上，进一步扩大了教学的知识的深度及广度，扩大了学生知识面",
              "教师课堂上的整体教学效果非常好，教师在教学方面极认真负责，教师的基本知识技能过硬",
              "教师能以饱满的精神为学生讲每一堂课。", "老师认真负责，以身为范",
              "教师的教学效果极佳，可以使同学在领略知识魅力的同时提高自己实际技能。教师教课内容广大博深，高质量，高效率。教课内容新颖，独特，有个性。",
              "老师知识丰富，上老师的课让我获益匪浅",
              "该老师风趣幽默，能很好的调节上课气疯，提高学生的上课积极性。讲课具有条理性，浅显易懂。",
              "教学态度认真，做事积极负责，有自己的风格，上课富有激情",
              "观点鲜明，对问题有自己独特的见解",
              "思路清晰、讲解逻辑性强",
              "老师授课的方式非常适合我们，他根据本课程知识结构的特点，重点突出，层次分明。",
              "老师上课有时非常幽默，有时非常严格，不过还是非常有教授风度的",
              "课堂内容充实，简单明了，使学生能够轻轻松松掌握知识。",
              "老师教学认真，课堂效率高，授课内容详细",
              "老师治学严谨，对学生严格要求。",
              "老师幽默风趣，上课气氛活跃。",
              "老师答疑认真，对同学们提出的问题能够详尽的解答，态度和蔼，十分有耐心",
              "老师讲课突出重点，内容详细，条理清晰，细致入微。",
              "老师授课认真，细致，能充分利用时间，形象条理",
              "老师讲课十分认真投入",
              "认真负责，严谨，耐心",
              "教学态度认真,讲课内容正确。教学内容贯通、严谨、科学。",
              "老师非常好哈",
              "对工作态度认真",
              "老师讲课十分投入,与同学和蔼可亲"
              ]

    # print("评教列表：" + "\n")
    centerure1 = "http://zhjw.scu.edu.cn/student/teachingEvaluation/teachingEvaluation/search"
    req2 = urllib.request.Request(centerure1)
    req2.add_header('User-Agent',
                    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36')
    req2data = urllib.request.urlopen(req2).read().decode("utf-8", "ignore")
    kcm = '"evaluationContent":"(.*?)"'
    skjs = '"evaluatedPeople":"(.*?)"'
    pg = '"isEvaluated":"(.*?)"'
    questionname = '"questionnaireName":"(.*?)",'
    questionnaireCoding = '"questionnaireCoding":"(.*?)"'
    evaluationContentNumbering = '"evaluationContentNumber":"(.*?)"'
    evaluatePeople = '"evaluatedPeople":"(.*?)"'
    type = '"typeName":"(.*?)"'
    questionnamesum = re.compile(questionname).findall(req2data)
    typeName = re.compile(type).findall(req2data)
    kcnum = re.compile(kcm).findall(req2data)
    skjsnum = re.compile(skjs).findall(req2data)
    pgnum = re.compile(pg).findall(req2data)
    questionnaireCode = re.compile(questionnaireCoding).findall(req2data)
    evaluationContentNumber = re.compile(evaluationContentNumbering).findall(req2data)
    evaluatePeopleNumber = re.compile(evaluatePeople).findall(req2data)

    print("课程名" + '\t' + "授课教师")  # +"\t"+"是否已评估")
    for i in range(0, len(kcnum)):
        pingjia = pingyu[random.randint(0, len(pingyu) - 1)]

        print(kcnum[i] + '\t' + skjsnum[
            2 * i])  # +'\t'+pgnum[i]+"\t"+questionnaireCode[i]+"\t"+evaluationContentNumber[i]+'\t'+evaluatePeopleNumber[i*2+1]+'\t'+questionnamesum[i])
        if pgnum[i] == '否':
            url = "http://zhjw.scu.edu.cn/student/teachingEvaluation/teachingEvaluation/evaluationPage"
            loginpostdata = urllib.parse.urlencode({
                "evaluatedPeople": skjsnum[2 * i],
                "evaluatedPeopleNumber": evaluatePeopleNumber[i * 2 + 1],
                "questionnaireCode": questionnaireCode[i],
                "questionnaireName": typeName[i],
                "evaluationContentNumber": evaluationContentNumber[i],
                "evaluationContentContent": "",
            }).encode('utf-8')
            req = urllib.request.Request(url, loginpostdata)
            req.add_header('Origin', 'http://zhjw.scu.edu.cn')
            req.add_header('User-Agent',
                           'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36')
            req.add_header('referer', 'http://zhjw.scu.edu.cn/student/teachingEvaluation/evaluation/index')
            reqdata3 = urllib.request.urlopen(req).read().decode("utf-8", "ignore")
            reqdata3 = re.sub(' +', '', reqdata3)
            reqdata3 = re.sub('\t', '', reqdata3)
            reqdata3 = reqdata3.replace('\r', '').replace('\n', '')
            # print(reqdata3)
            token1 = '"radio"class="ace"name="(.*?)"'
            token = 'id="tokenValue"value="(.*?)"'
            tokens = re.compile(token1).findall(str(reqdata3))
            h = set()
            tokensnew = list()
            m = 0
            for j in range(0, len(tokens)):
                if h.__contains__(tokens[j]):
                    m
                else:
                    tokensnew.append(tokens[j])
                    h.add(tokens[j])
            tokens = tokensnew
            # print("tokens",tokens)
            tokenvalue = re.compile(token).findall(str(reqdata3))
            # print("tokenvalue",tokenvalue)

            pingjiaourl = "http://zhjw.scu.edu.cn/student/teachingEvaluation/teachingEvaluation/evaluation"

            try:
                loginpostdata = urllib.parse.urlencode({
                    "tokenValue": tokenvalue[0],
                    "questionnaireCode": questionnaireCode[i],
                    "evaluationContentNumber": evaluationContentNumber[i],
                    "evaluatedPeopleNumber": evaluatePeopleNumber[i * 2 + 1],
                    "count": 0,
                    tokens[0]: "10_1",
                    tokens[1]: "10_1",
                    tokens[2]: "10_1",
                    tokens[3]: "10_1",
                    tokens[4]: "10_1",
                    tokens[5]: "10_1",
                    tokens[6]: "10_1",
                    "zgpj": pingjia,
                }).encode('utf-8')
            except Exception:
                loginpostdata = urllib.parse.urlencode({
                    "tokenValue": tokenvalue[0],
                    "questionnaireCode": questionnaireCode[i],
                    "evaluationContentNumber": evaluationContentNumber[i],
                    "evaluatedPeopleNumber": evaluatePeopleNumber[i * 2 + 1],
                    "count": 0,
                    tokens[0]: "10_1",
                    tokens[1]: "10_1",
                    tokens[2]: "10_1",
                    tokens[3]: "10_1",
                    tokens[4]: "10_1",
                    tokens[5]: "10_1",
                    "zgpj": pingjia,
                }).encode('utf-8')

            reqpingjiao = urllib.request.Request(pingjiaourl, loginpostdata)
            req.add_header('Origin', 'http://zhjw.scu.edu.cn')
            req.add_header('User-Agent',
                           'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36')
            req.add_header('referer',
                           'http://zhjw.scu.edu.cn/student/teachingEvaluation/teachingEvaluation/evaluationPage')
            reqdata4 = urllib.request.urlopen(reqpingjiao).read().decode("utf-8", "ignore")
            print("评教结果：" + reqdata4)
            time.sleep(120)

        else:
            print("这门课已经评价过了")


for i in range(10):
    cjar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cjar))
    urllib.request.install_opener(opener)
    urlbegin = "http://zhjw.scu.edu.cn/login"

    reqdatalogin = urllib.request.urlopen(urlbegin).read().decode("utf-8", "ignore")
    s = urllib.request.urlopen(urlbegin)
    CaptchaUrl = "http://zhjw.scu.edu.cn/img/captcha.jpg"
    picture = opener.open(CaptchaUrl).read()
    # 用openr访问验证码地址,获取cookie
    local = open(os.getcwd() + '/test.jpg', 'wb')
    local.write(picture)
    local.close()
    # im = pytesseract.image_to_string('e:/image.jpg')
    # print("验证码"+im)

    # print("四川大学教务系统模拟登录系统")



    # 以下进入自动登录部分
    j_captchal = recognition.main()  # input()#input("请输入验证码：")
    loginposturl = "http://zhjw.scu.edu.cn/j_spring_security_check"
    loginpostdata = urllib.parse.urlencode({
        "j_username": username,
        "j_password": password,
        "j_captcha": j_captchal,
    }).encode('utf-8')
    req = urllib.request.Request(loginposturl, loginpostdata)
    req.add_header('Origin', 'http://zhjw.scu.edu.cn')
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36')
    req.add_header('referer', 'http://zhjw.scu.edu.cn/login')
    reqdatalogin = urllib.request.urlopen(req).read().decode("utf-8", "ignore")
    checklogin = 'URP综合(.*?)首页'
    checkanswer = re.compile(checklogin).findall(reqdatalogin)
    if len(checkanswer) != 0:

        print("success")
        pjcx()
        break
    else:
        print("fail")

