# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import re
import math
import jieba


def read_stop():
    global stop
    with open("cn_stopwords.txt", "r", encoding="utf-8") as file:
        stop = file.read()
    stop = stop.split()


def unigram_character(name):
    path = "Data/" + name + ".txt"

    with open(path, "r", encoding="utf-8") as file:
        data = file.read()
    data = data.replace('本书来自www.cr173.com免费txt小说下载站', '')  # 去除网站广告
    data = data.replace('更多更新免费电子书请关注www.cr173.com', '')
    data = re.sub('[^\u4e00-\u9fa5]+', '', data)  # 只保留中文字符
    result = [one for one in data]  # 按字分割

    L = 0
    cnt = {}
    for char in result:  # 字频统计
        if char not in stop:
            cnt[char] = cnt.get(char, 0) + 1
    en = 0
    for i in cnt.items():  # 计算总字数
        L += i[1]

    for i in cnt.items():
        p = i[1] / L
        en += -p * math.log(p, 2)
    print(name + '字一元模型:', en)
    with open('output.csv', "a", encoding="GBK") as file:
        file.write(name + ' 字 一元模型: ' + str(en) + '\n')

    global Cnt_character_1  # 存入全局变量，供多元模型计算使用
    Cnt_character_1 = cnt


def bigram_character(name):
    path = "Data/" + name + ".txt"

    with open(path, "r", encoding="utf-8") as file:
        data = file.read()
    data = data.replace('本书来自www.cr173.com免费txt小说下载站', '')
    data = data.replace('更多更新免费电子书请关注www.cr173.com', '')
    data = re.sub('[^\u4e00-\u9fa5]+', '', data)

    for i in stop:
        data = data.replace(i, '')  # 去除停词

    result = []
    for i in range(0, len(data) - 1):
        result.append(data[i] + data[i + 1])  # 二元模型
    L = 0
    cnt = {}
    for char in result:
        cnt[char] = cnt.get(char, 0) + 1  # 二元模型字频统计
    en = 0
    for i in cnt.items():
        L += i[1]
    for i in cnt.items():
        p1 = i[1] / L
        cnt2 = Cnt_character_1[i[0][0]]
        en += -p1 * math.log(i[1] / cnt2, 2)
    print(name + '字二元模型:', en)
    with open('output.csv', "a", encoding="GBK") as file:
        file.write(name + ' 字 二元模型: ' + str(en) + '\n')
    global Cnt_character_2  # 存入全局变量，供多元模型计算使用
    Cnt_character_2 = cnt


def trigram_character(name):
    path = "Data/" + name + ".txt"

    with open(path, "r", encoding="utf-8") as file:
        data = file.read()
    data = data.replace('本书来自www.cr173.com免费txt小说下载站', '')
    data = data.replace('更多更新免费电子书请关注www.cr173.com', '')
    data = re.sub('[^\u4e00-\u9fa5]+', '', data)

    for i in stop:
        data = data.replace(i, '')

    result = []
    for i in range(0, len(data) - 2):
        result.append(data[i] + data[i + 1] + data[i + 2])
    L = 0
    cnt = {}
    for char in result:
        cnt[char] = cnt.get(char, 0) + 1
    en = 0
    for i in cnt.items():
        L += i[1]
    for i in cnt.items():
        p1 = i[1] / L
        cnt2 = Cnt_character_2[i[0][0] + i[0][1]]
        en += -p1 * math.log(i[1] / cnt2, 2)
    print(name + '字三元模型:', en)
    with open('output.csv', "a", encoding="GBK") as file:
        file.write(name + ' 字 三元模型: ' + str(en) + '\n')


def unigram_word(name):
    path = "Data/" + name + ".txt"
    with open(path, "r", encoding="utf-8") as file:
        data = file.read()
    data = data.replace('本书来自www.cr173.com免费txt小说下载站', '')
    data = data.replace('更多更新免费电子书请关注www.cr173.com', '')
    data = data.replace('\n', '')
    data = data.replace('\u3000', '')
    data = data.replace(' ', '')

    data = jieba.lcut(data)  # 使用jieba分词
    data = [val for val in data if val not in stop]  # 去除停词
    L = 0
    cnt = {}
    for char in data:
        cnt[char] = cnt.get(char, 0) + 1  # 词频统计
    en = 0
    for i in cnt.items():
        L += i[1]

    for i in cnt.items():
        p = i[1] / L
        en += -p * math.log(p, 2)
    print(name + '词一元模型', en)
    global Cnt_word_1
    Cnt_word_1 = cnt
    with open('output.csv', "a", encoding="GBK") as file:
        file.write(name + ' 词 一元模型: ' + str(en) + '\n')


def bigram_word(name):
    path = "Data/" + name + ".txt"
    with open(path, "r", encoding="utf-8") as file:
        data = file.read()
    data = data.replace('本书来自www.cr173.com免费txt小说下载站', '')
    data = data.replace('更多更新免费电子书请关注www.cr173.com', '')
    data = data.replace('\n', '')
    data = data.replace('\u3000', '')
    data = data.replace(' ', '')

    data = jieba.lcut(data)
    data = [val for val in data if val not in stop]  # 去除停词
    result = []
    for i in range(0, len(data) - 1):
        result.append((data[i], data[i + 1]))  # 生成二元模型

    L = 0
    cnt = {}
    for char in result:
        cnt[char] = cnt.get(char, 0) + 1
    en = 0
    for i in cnt.items():
        L += i[1]

    for i in cnt.items():
        p1 = i[1] / L
        cnt2 = Cnt_word_1[i[0][0]]
        en += -p1 * math.log(i[1] / cnt2, 2)

    print(name + '词二元模型', en)
    global Cnt_word_2
    Cnt_word_2 = cnt

    with open('output.csv', "a", encoding="GBK") as file:
        file.write(name + ' 词 二元模型: ' + str(en) + '\n')


def trigram_word(name):
    path = "Data/" + name + ".txt"
    with open(path, "r", encoding="utf-8") as file:
        data = file.read()
    data = data.replace('本书来自www.cr173.com免费txt小说下载站', '')
    data = data.replace('更多更新免费电子书请关注www.cr173.com', '')
    data = data.replace('\n', '')
    data = data.replace('\u3000', '')
    data = data.replace(' ', '')

    data = jieba.lcut(data)
    data = [val for val in data if val not in stop]
    result = []
    for i in range(0, len(data) - 2):
        result.append((data[i], data[i + 1], data[i + 2]))

    L = 0
    cnt = {}
    for char in result:
        cnt[char] = cnt.get(char, 0) + 1
    en = 0
    for i in cnt.items():
        L += i[1]

    for i in cnt.items():
        p1 = i[1] / L
        cnt2 = Cnt_word_2[(i[0][0], i[0][1])]
        en += -p1 * math.log(i[1] / cnt2, 2)

    print(name + '词三元模型', en)
    with open('output.csv', "a", encoding="GBK") as file:
        file.write(name + ' 词 三元模型: ' + str(en) + '\n')


if __name__ == '__main__':
    read_stop()  # 读入停词表
    with open('Data/inf.txt', "r", encoding="utf-8") as file:  # 读入目录
        menu = file.read()
    menu = menu.split(',')
    tem = ''
    for i in menu:  # 将所有小说纳入一个文件以计算所有文字的信息熵
        with open('Data/' + i + '.txt', "r", encoding="utf-8") as file:
            tem += file.read()
        with open('Data/所有小说.txt', "w", encoding="utf-8") as file:
            file.write(tem)
        with open('output.csv', "w", encoding="GBK") as file:
            file.truncate(0)
    menu.append('所有小说')
    for i in menu:
        unigram_character(i)  # 计算字一元模型信息熵
        bigram_character(i)  # 计算字二元模型信息熵
        trigram_character(i)  # 计算字三元模型信息熵
        unigram_word(i)  # 计算词一元模型信息熵
        bigram_word(i)  # 计算词二元模型信息熵
        trigram_word(i)  # 计算词三元模型信息熵
