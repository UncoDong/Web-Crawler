# -*- coding: utf-8 -*-
# @Time    : 2020/09/24
# @Author  : UncoDong
# @Cnblogs : https://blog.csdn.net/weixin_42763696


# 打开
import pickle
import sys
import os

if __name__ == '__main__':


    # 这里修改类型名称
    #type_name = sys.argv[1]
    type_name = 'baobeixunjia'
    
    # 从'filname.pickle'读取
    print('打开', 'ID_all\{0}_ID.pickle'.format(type_name))
    with open('ID_all\{0}_ID.pickle'.format(type_name), 'rb') as fp:
        length = len(pickle.load(fp))

    print(length)
    start_num = 0 # 区间头
    end_num = 1000 # 区间尾
    change_num = 1000 # 区间大小

    while end_num<= length:
        command = 'python .\get_all_information_async_py.py {0} {1} {2}'.format(start_num,end_num,type_name)
        print(command)
        
        # 命令行执行
        os.system(command)

        # 区间改变
        start_num = start_num + change_num
        end_num = end_num + change_num
