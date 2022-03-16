import re

def StarStatistic(path:str):
    with open(path, 'r', encoding='utf8') as f:
        all_data = f.readlines()
    star_list = []
    for index, data in enumerate(all_data):
        data = eval(data)
        star = data["star"]
        if star == None:
            continue
        star = re.findall('sml-rank-stars sml-str(\d+) star', str(star))[0]
        star_list.append(eval(star))
    result = sum(star_list)
    average = result / len(star_list)
    print('Average:%f' % average)

if __name__ == '__main__':
    StarStatistic('泰山大众点评.txt')