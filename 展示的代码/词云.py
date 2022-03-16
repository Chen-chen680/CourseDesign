import jieba
import glob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
import numpy as np
from PIL import Image
import cv2
from random import randint

DATA_PATH = R'C:\Users\12517\Desktop\大数据课程设计\泰山大众点评.txt'
STOP_WORDS_DIR = R'C:\Users\12517\Desktop\大数据课程设计\代码\文本分析\stopwords'

def ReadData(path:str):
    '''读取数据
    ::param:path
    ::return generator [name:用户名； data_time：用户评价时间; star:用户评级; comment:评论正文]
    '''
    with open(path, 'r', encoding='utf8') as f:
        data_list = f.readlines()
        for index, data in enumerate(data_list):
            data_list[index] = eval(data)
        return data_list

def DataCommentGet(save_path:str):
    data_list = ReadData(DATA_PATH)
    with open(save_path, 'w', encoding='utf8') as f:
        for data in data_list:
            comment = data['comment'].replace('收起评价', '')
            f.write(comment)

def random_color_func(word=None, font_size=None, position=None, orientation=None, font_path=None, random_state=None):
    h = randint(120,250)
    s = int(100.0 * 255.0 / 255.0)
    l = int(100.0 * float(randint(60, 120)) / 255.0)
    return "hsl({}, {}%, {}%)".format(h, s, l)

def CiYunDraw(comment_path:str):
    '''绘制词云'''
    stopwords_set = Read_Stop()
    mask = np.array(Image.open(r'C:\Users\12517\Desktop\大数据课程设计\代码\文本分析\mask1.jpg').convert('L'))
    mask[mask > 127] = 255
    mask[mask <= 127] = 0
    mask = cv2.resize(mask, (1200, 2000))
    with open(comment_path, 'r', encoding='utf8') as f:
        comment = f.read()
        comment = comment.replace('\n', '')
        result = WordCloud(font_path='仿宋_gb2312.ttf',
                           max_words=400,
                           scale=2,
                           mask=mask,
                           background_color='white',
                           stopwords=stopwords_set).generate(comment)
        plt.imshow(result, interpolation= 'bilinear')
        plt.axis('off')
        plt.show()
        result.to_file('out1.png')

def Read_Stop():
    stop_words_list = glob.glob(os.path.join(STOP_WORDS_DIR, '*.txt'))
    store_set = list()
    for stop_words_path in stop_words_list:
        with open(stop_words_path, 'r', encoding='utf8') as f:
            result = f.readlines()
            store_set += result
    store_set = map(lambda x: x.replace('\n', ''), store_set)
    store_set = set(store_set)
    return store_set

if __name__ == '__main__':
    CiYunDraw('Only_comment.txt')