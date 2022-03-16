from pyecharts.charts import Line, Pie, Bar
import pyecharts.options as opts
from pyecharts.faker import Faker
import numpy as np

def ReadData(path:str):
    reverse_list = []
    with open(path, 'r', encoding='utf-8-sig') as f:
        data = f.readlines()
    for index, one_data in enumerate(data):
        data[index] = one_data.replace('\n', '').split(',')
        if index == 0:
            continue
        data[index][1], data[index][2], data[index][3], data[index][4], data[index][5], data[index][6] = int(data[index][1]), int(data[index][2]), int(data[index][3]), int(data[index][4]), int(data[index][5]), int(data[index][6])
    data.reverse()
    return data[1: len(data) - 1]

def PlotCovidData(All_data:list):
    date, SumConfirm, OutInputCovid, SumRecovery, SumDeath, Isolation, Obeserved = [], [], [], [], [], [], []
    for data in All_data:
        SumConfirm.append(data[1])
        OutInputCovid.append(data[2])
        SumConfirm.append(data[3])
        SumDeath.append(data[4])
        Isolation.append(data[5])
        Obeserved.append(data[6])
        date.append(data[0])
    line1 = (
        Line()
            .set_global_opts(tooltip_opts=opts.TooltipOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(type_="category"),
            yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            splitline_opts=opts.SplitLineOpts(is_show=True)))
        .add_xaxis(date)
        .add_yaxis('累计确诊', SumConfirm, label_opts=opts.LabelOpts(is_show=False))
        .add_yaxis('境外输入', OutInputCovid, label_opts=opts.LabelOpts(is_show=False))
        .add_yaxis('累计治愈', SumRecovery, label_opts=opts.LabelOpts(is_show=False))
        .add_yaxis('累计死亡', SumDeath, label_opts=opts.LabelOpts(is_show=False))
        .add_yaxis('在医院隔离', Isolation, label_opts=opts.LabelOpts(is_show=False))
        .add_yaxis('尚在观察', Obeserved, label_opts=opts.LabelOpts(is_show=False))
    )
    line1.render('SichuanCovid.html')

def SentimentAverage(path:str):
    with open(path, 'r', encoding='utf-8-sig') as f:
        all_data = f.readlines()
    positive_list = []
    for index, data in enumerate(all_data):
        if index == 0:
            continue
        all_data[index] = all_data[index].replace('\n','').split(',')
        if len(all_data[index]) > 6:
            continue
        positive = eval(all_data[index][3])
        positive_list.append(positive)
    average_positive = sum(positive_list) / len(positive_list)
    PiePlot(average_positive)

def PiePlot(data):
    '''
    :param data: 情感分析的积极分数
    '''
    positive = data
    negative = 1 - data
    pie = Pie()
    data_dict = [('消极', negative), ('积极', positive)]
    pie.add(
        series_name='',
        data_pair=data_dict
    )
    pie.render('pie.html')

def BarStarPlot(path:str):
    star_list = []
    with open(path, 'r', encoding='utf8') as f:
        all_data = f.readlines()
    for index, data in enumerate(all_data):
        all_data[index] = eval(data)
        star_list.append(eval(data)['star'])
    bar_y_list = [star_list.count('sml-rank-stars sml-str10 star'), star_list.count('sml-rank-stars sml-str20 star'), star_list.count('sml-rank-stars sml-str30 star'), star_list.count('sml-rank-stars sml-str40 star'), star_list.count('sml-rank-stars sml-str50 star')]
    bar = (
        Bar()
        .add_xaxis(['10分', '20分', '30分', '40分', '50分'])
        .add_yaxis('评分', bar_y_list)
        .set_global_opts(title_opts=opts.TitleOpts(title='用户评分'))
    )
    bar.render('用户评分直方图.html')

def BarSentimentPlot(path:str):
    negative_list = []
    with open(path, 'r', encoding='utf-8-sig') as f:
        all_data = f.readlines()
    for index, data in enumerate(all_data[1:]):
        data = data.split(',')
        negative_list.append(data[-2])
    sentiment_class_list = []
    for index, negative_score in enumerate(negative_list):
        if eval(negative_score) <= 0.33:
            sentiment_class_list.append('积极')
        elif eval(negative_score) <= 0.66 and eval(negative_score) > 0.33:
            sentiment_class_list.append('中性')
        else:
            sentiment_class_list.append('消极')

    bar_y_list = [sentiment_class_list.count('消极'), sentiment_class_list.count('中性'), sentiment_class_list.count('积极')]
    bar = (
        Bar()
        .add_xaxis(['消极', '中性', '积极'])
        .add_yaxis('情感分析结果', bar_y_list)
        .set_global_opts(title_opts=opts.TitleOpts(title='泰山评论情感分析'))
    )
    bar.render('情感分析直方图.html')


def PearsonCor(star_path:str, sentiment_path:str):
    user_dict = {}
    with open(star_path, 'r', encoding='utf-8') as f:
        star_data = f.readlines()
    for index, one_data in enumerate(star_data):
        one_data = eval(one_data)
        if one_data['star'] == None:
            continue
        user, star = one_data['name'], ''.join([x for x in one_data['star'] if x.isdigit()])
        user_dict[user] = [eval(star)]
    user_list = list(user_dict.keys())
    with open(sentiment_path, 'r', encoding='utf-8-sig') as f:
        sentiment_all_data = f.readlines()
    for index, one_data in enumerate(sentiment_all_data[1:]):
        one_data = one_data.split(',')
        user = one_data[0]
        positive = 1 - eval(one_data[-2])
        if user in user_list:
            user_dict[user].append(positive)
        else:
            continue
    star_list, sentiment_list = [], []
    for user in user_list:
        if len(user_dict[user]) == 2:
            star_list.append(user_dict[user][0])
            sentiment_list.append(user_dict[user][1])
        else:
            continue
    Xmean = np.mean(star_list)
    Ymean = np.mean(sentiment_list)
    XSD = np.std(star_list)
    YSD = np.std(sentiment_list)
    ZX, ZY = (star_list - Xmean) / XSD, (sentiment_list - Ymean)/ YSD
    r = np.sum(ZX * ZY / len(star_list))
    print('Pearson相关系数为：%f' % r)

if __name__ == '__main__':
    # SentimentAverage(r'C:\Users\12517\Desktop\大数据课程设计\代码\文本分析\SentimentAnalysis.csv')
    # data = ReadData(r'C:\Users\12517\Desktop\大数据课程设计\代码\四川疫情数据.csv')
    # PlotCovidData(data)
    # BarPlot(r'C:\Users\12517\Desktop\大数据课程设计\代码\文本分析\泰山大众点评.txt')
    # BarSentimentPlot(r'C:\Users\12517\Desktop\大数据课程设计\代码\文本分析\SentimentAnalysis.csv')
    PearsonCor(star_path=r'C:\Users\12517\Desktop\大数据课程设计\代码\文本分析\泰山大众点评.txt', sentiment_path=r'C:\Users\12517\Desktop\大数据课程设计\代码\文本分析\SentimentAnalysis.csv')