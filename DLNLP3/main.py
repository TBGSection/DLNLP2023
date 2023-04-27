import jieba
import re
import random
import numpy as np
from sklearn.cluster import KMeans


def read(menu):
    data = []

    for name in menu:
        data_1 = []
        path = 'Data/' + name + '.txt'
        with open(path, 'r', encoding='ANSI') as read_file:
            read_cu = read_file.read()
            read_cu = Remove(read_cu)
            read_list = list(read_cu)
            cut = int(len(read_cu) // 13)
            for i in range(13):
                data_0 = read_list[i * cut + 1:i * cut + 500]
                data_1 = data_1 + read_list[i * cut + 501:i * cut + 1000]
                data.append(data_0)
            # print(read_list)
            print(name)
            read_file.close()

    return data


def Remove(txt):
    ad = ['本书来自www.cr173.com免费txt小说下载站\n更多更新免费电子书请关注www.cr173.com', '----〖新语丝电子文库(www.xys.org)〗', '新语丝电子文库']
    for i in ad:  # 去广告
        txt = txt.replace(i, '')

    with open("cn_stopwords.txt", "r", encoding="utf-8") as file:
        stop = file.read()
    stop = stop.split()

    word_flag = 1 #按词或者字
    if word_flag == 1:
        txt = jieba.lcut(txt)
    else:
        txt = [one for one in txt]
    txt = [val for val in txt if val not in stop]  # 去除停词

    txt = [i for i in txt if not re.findall("[^\u4e00-\u9fa5]+", i)]

    return txt

if __name__ == '__main__':

    with open('Data/inf.txt', "r", encoding="ANSI") as file:  # 读入目录
        menu = file.read()
    menu = menu.split(',')
    data = read(menu)
    topic_num = 40  # topic 数量
    topic_set = []  # 所有topic合集
    topic_cnt = {}  # 每个topic词数
    alltopic = []  # 所有文章词的topic序列
    alltopic_dis = []  # 所有文章各个topic的数量
    word_cnt = []  # 所有文章的总词数
    # 生成topic
    for i in range(topic_num):
        topics = {}
        topic_set.append(topics)
    print(topic_set)
    print(topic_set[1])
    # 初始化
    for txt in data:
        topic = []  # 文章词的topic序列
        topic_dis = {}  # 每篇文章各个topic的数量
        for word in txt:
            a = random.randint(0, topic_num - 1)  # 初始随机生成一个topic
            topic.append(a)
            topic_cnt[a] = topic_cnt.get(a, 0) + 1
            topic_dis[a] = topic_dis.get(a, 0) + 1
            topic_set[a][word] = topic_set[a].get(word, 0) + 1
        alltopic.append(topic)
        topic_dis = list(
            dict(sorted(topic_dis.items(), key=lambda x: x[0], reverse=False)).values())  # 每篇文章各个topic的数量,排序并转化为list
        alltopic_dis.append(topic_dis)
        word_cnt.append(sum(topic_dis))
    print(topic_cnt)
    topic_cnt = list(dict(sorted(topic_cnt.items(), key=lambda x: x[0], reverse=False)).values())
    print('topic_cnt')
    print(topic_cnt)

    ## 转为array
    alltopic_dis = np.array(alltopic_dis)
    topic_cnt = np.array(topic_cnt)
    word_cnt = np.array(word_cnt)

    # 总字典
    All_topics = {}
    for i in range(topic_num):
        All_topics.update(topic_set[i])
    K = len(All_topics)
    print('K', K)

    topic_p = []  # 文章选中topic的概率
    topic_p_t = []
    for i in range(len(data)):
        p = np.divide(alltopic_dis[i], word_cnt[i])
        topic_p.append(p)
    topic_p = np.array(topic_p)

    stop = 0  # 迭代停止标志
    loopcount = 0  # 迭代次数
    while loopcount <= 35:  # 使用迭代次数控制循环
        # while stop == 0:

        i = 0
        for txt in data:
            topic = alltopic[i]  # 当前文章词topic序列
            for w in range(len(txt)):
                word = txt[w]
                p = []  # 该词由各个topic生成的概率
                n_topic2word = []  # 各个topic生成该词的频率
                p_topic2word = []  # 各个topic生成该词的概率
                for k in range(topic_num):
                    n_topic2word.append(topic_set[k].get(word, 0))
                n_topic2word = np.array(n_topic2word)
                alpha = 0.01
                beta = 0.1
                p_topic2word = (n_topic2word + beta) / (topic_cnt + K * beta)
                p = (topic_p[i] + alpha) * p_topic2word

                # p_topic2word = n_topic2word / topic_cnt
                # p = topic_p[i] * p_topic2word

                # max = np.argmax(p)  # 生成该词最大可能的topic
                max = np.random.choice(topic_num, p=p / p.sum())
                # if max!=topic[w]:
                #    print('changed')

                ## 更新各文章中各topic数量
                alltopic_dis[i][topic[w]] -= 1
                alltopic_dis[i][max] += 1
                ## 更新每个topic的总词数
                topic_cnt[topic[w]] -= 1
                topic_cnt[max] += 1
                ## 更新各个topic 内容
                topic_set[topic[w]][word] = topic_set[topic[w]].get(word, 0) - 1
                topic_set[max][word] = topic_set[max].get(word, 0) + 1
                ## 新topic序列
                topic[w] = max
            alltopic[i] = topic
            i += 1
        loopcount += 1
        if loopcount == 1:  # 更新新的文章对topic概率
            for i in range(len(data)):
                p = np.divide(alltopic_dis[i], word_cnt[i])
                topic_p_t.append(p)
            topic_p_t = np.array(topic_p_t)
        else:
            for i in range(len(data)):
                p = np.divide(alltopic_dis[i], word_cnt[i])
                topic_p_t[i] = p
        if (topic_p_t == topic_p).all():
            stop = 1
        else:
            topic_p = topic_p_t.copy()
        print('current loop :', loopcount)

    for i in range(topic_num):
        print('this is topic ', i)
        a = topic_set[i]
        res = {}
        for key, value in a.items():  # 每个topic降序排序
            if value != 0:
                res[key] = value
        res = list(sorted(res.items(), key=lambda x: x[1], reverse=True))
        print(res[:25])  # 输出前25个最多的主题词
    print('result')
    print(topic_p_t)

    print('down,this loop:', loopcount)

    cluster = KMeans(n_clusters=16)  # K-means聚类
    cluster.fit(topic_p_t)

    labels = cluster.labels_
    for i in range(len(labels)):
        print(labels[i], end=' ')
        if (i + 1) % 13 == 0:
            print('\n')
