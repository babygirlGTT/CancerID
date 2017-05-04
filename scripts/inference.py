# -*- coding: utf-8 -*-  
import json

# 返回a与b差集(a-b)
def diff_set(a, b):
    diff_list = list(set(a) - (set(b)))
    result = [{i:val} for i,val in enumerate(diff_list)]
    return result 
# 返回a和b交集
def inter_set(a, b):
    inter_list = list(set(a) & (set(b)))
    result = [{i:val} for i,val in enumerate(inter_list)]
    return result 