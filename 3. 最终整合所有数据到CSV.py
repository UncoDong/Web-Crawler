# -*- coding: utf-8 -*-
# @Time    : 2020/09/24
# @Author  : UncoDong
# @Cnblogs : https://blog.csdn.net/weixin_42763696


import os
import pickle
# 将所有数据压缩到一行
from itertools import chain
import pandas as pd
import sys

if __name__ == '__main__':

    # 这里修改类型名称
    #type_name = sys.argv[1]
    type_name = 'baobeixunjia'

    # 打开保存pickle的文件
    dir_name = 'pickle_all\pickle_{0}'.format(type_name)
    pickle_list = os.listdir(dir_name)
    print('开始遍历{0}, 共{1}个文件'.format(dir_name,len(pickle_list)))

    # 所有信息的字典
    information_dic = []

    # 遍历pickle
    for pickle_name in pickle_list:
        with open('{0}/{1}'.format(dir_name,pickle_name), 'rb') as fp:
            information_dic.append(pickle.load(fp))

    # 使用pandas存入CSV
    df = pd.DataFrame(list(chain(*information_dic)))
    csv_path = 'CSV_all\{0}.csv'.format(type_name)
    df.to_csv(csv_path, encoding="utf_8_sig")

    # 修改分隔符
    import csv
    reader = list(csv.reader(open(csv_path, "rU",encoding='utf-8'), delimiter=',')) # 原来的分隔符
    with open(csv_path, 'w',encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t') # 现在的分隔符
        writer.writerows(row for row in reader)

