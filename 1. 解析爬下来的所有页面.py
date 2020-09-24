# -*- coding: utf-8 -*-
# @Time    : 2020/09/24
# @Author  : UncoDong
# @Cnblogs : https://blog.csdn.net/weixin_42763696


from bs4 import BeautifulSoup

global all_ID_list

import sys
'''
Summary:
    通过文件名获取每个文件内的所有ID
Parameters:
    page_file_name - 文件名
Return；
    没有
'''
def analyse_each_page(page_file_name,dir_name):
    # 打开文件，取出HTML文本
    with open('{1}/{0}'.format(page_file_name,dir_name),'r',encoding='utf-8') as fp:
        page_text = fp.read()
        
    # 扔到汤里
    soup = BeautifulSoup(page_text,'lxml')
        
    # 所有tr的列表
    tr_list = soup.select('body form#form1 table#GridView1 tbody tr')
    
    # 遍历所有tr
    for tr in tr_list:
        text = None
        try:
            text = "".join(tr.select('td')[0].text.split())
            #print(text)
            # 看是否是数字
            num = float(text) 
            all_ID_list.append(text)       
        except:
            #print(text)
            continue

if __name__ == '__main__':
    
    import time
    start_time = time.time()

    # 所有ID的列表
    all_ID_list = []

    # 读取页面文件列表，这里修改类型名称
    import os
    #type_name = sys.argv[1]
    type_name = 'baobeixunjia'
    
    dir_name = 'save_pages_all/save_pages_{0}'.format(type_name)
    print('开始解析',dir_name)
    pages_list = os.listdir(dir_name)

    # 遍历每一个文件
    for page_file_name in pages_list:
        all_ID_list.append(analyse_each_page(page_file_name,dir_name))

    # 去除所有的None
    while None in all_ID_list:
        all_ID_list.remove(None)
        
    import pickle
    # 保存到pickle
    with open('ID_all/{0}_ID.pickle'.format(type_name), 'wb') as fp:
        pickle.dump(all_ID_list, fp)
        
    print('保存到{0},共{1}条数据'.format('ID_all/{0}_ID.pickle'.format(type_name), len(all_ID_list)))
        
    end_time = time.time()
    print('用时 %d second'%(end_time-start_time))
