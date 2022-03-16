# from pyecharts import Map

province_distribution = {'山东':1806,
                         '贵州':250,
                         '江西':335,
                         '重庆':287,
                         '内蒙古':289,
                         '湖北':463,
                         '辽宁':491,
                         '湖南':441,
                         '福建':389,
                         '上海':648,
                         '北京':1104,
                         '广西':299,
                         '广东':1006,
                         '四川':535,
                         '云南':252,
                         '江苏':1110,
                         '浙江':728,
                         '青海':82,
                         '宁夏':162,
                         '河北':974,
                         '黑龙江':363,
                         '吉林':144,
                         '天津':430,
                         '陕西':434,
                         '甘肃':244,
                         '新疆':202,
                         '河南':996,
                         '安徽':617,
                         '山西':492,
                         '海南':0,
                         '台湾':59,
                         '西藏':66,'香港':126,'澳门':57,'其他':0}
keys = list(province_distribution.keys())
with open('map.csv', 'w', encoding='utf-8-sig') as f:
    for key in keys:
        f.write('%s,%s\n' % (key, str(province_distribution[key])))

# provice = list(province_distribution.keys())
# values = list(province_distribution.values())
# map = Map("中国地图", '中国地图', width=1200, height=600)
# map.add("", provice, values, visual_range=[0, 2000], maptype='china', is_visualmap=True,
#         visual_text_color='#000')
# map.render(path="中国地图.html")