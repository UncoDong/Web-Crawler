# -*- coding: utf-8 -*-
# @Time    : 2020/09/24
# @Author  : UncoDong
# @Cnblogs : https://blog.csdn.net/weixin_42763696


# 导入分析库
from bs4 import BeautifulSoup
# 导入通用爬虫python基本库
import requests
# 导入正则匹配
import re
# 将所有数据压缩到一行
from itertools import chain
# http 协程
import aiohttp
# 协程
import asyncio

# User-Agent 保护
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
}

global start_num
global end_num

start_num = 0
end_num = 1000


# 打开
import pickle
import sys
import os



import time
from aiohttp import ClientSession, TCPConnector, client_exceptions

loop = asyncio.get_event_loop()

async def get_information_from_aspx_url(session, url):

    # 提取信息到字典
    information_dic = {}

    while information_dic == {}:
        try:
            # print("发送请求：", url)
            async with session.get(url, verify_ssl=False) as response:
                text = await response.text()
                # print(url,'获得text')
                # 将每一页的HTML信息存入beautifulsoup，等待分析
                soup = BeautifulSoup(text, 'lxml')
            
                
                for each in soup.select('body div#table_1 div.reginfo ul li'):
                    messages = each.text.split("：")
                    # 防止出现'姓\xa0\xa0\xa0\xa0名' 的情况
                    key = "".join(messages[0].split())
                    value = "".join(messages[1].split())
                    information_dic[key] = value
                
                all_information_list.append(information_dic)
                # print('得到了',url)
        except:
            # print(url,'重新发送')
            # import traceback
            # traceback.print_exc()
            continue
            
        
async def main():
    timeout = aiohttp.ClientTimeout(total=330, connect=2, sock_connect=15, sock_read=10)
    async with aiohttp.ClientSession(connector=TCPConnector(limit=400), timeout=timeout) as session:

        # for url in all_aspx_url_list:
        #    await asyncio.wait(loop.create_task(get_information_from_aspx_url(session, url)))
            
        tasks = [loop.create_task(get_information_from_aspx_url(session, url)) for url in all_aspx_url_list]#[begin_index:end_index]]

        await asyncio.wait(tasks)


if __name__ == '__main__':
    try:
        start_num = int(sys.argv[1])

        end_num = int(sys.argv[2])

        type_name = sys.argv[3]

        print('读取{0}到{1}的数据'.format(start_num, end_num))
        
        
        # 从'filname.pickle'读取
        print('打开', 'ID_all/{0}_ID.pickle'.format(type_name))
        with open('ID_all/{0}_ID.pickle'.format(type_name), 'rb') as fp:
            all_ID_list = pickle.load(fp)


        all_aspx_url_list = []
        # 获得所有url
        for ID in all_ID_list:
            all_aspx_url_list.append('https://www.baobeihuijia.com/view.aspx?id={0}'.format(ID))
        print('all_aspx_url_list',len(all_aspx_url_list))
        # print(all_aspx_url_list[:10])
        all_aspx_url_list = all_aspx_url_list[start_num : end_num]

        # 所有信息的字典
        all_information_list = []



        start = time.clock()
        
        loop.run_until_complete(main())

        elapsed = (time.clock() - start)
        print("Time used:",elapsed)

        with open('pickle_all/pickle_{0}/{1}-{2}.pickle'.format(type_name, start_num, end_num), 'wb') as fp:
            pickle.dump(all_information_list, fp)
    except:
        import traceback
        traceback.print_exc()
    

        
    # import pandas as pd
    # df = pd.DataFrame(all_information_list)

    # df.to_csv('Result_async.csv',encoding="utf_8_sig") 
    
    
