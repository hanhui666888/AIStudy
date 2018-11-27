import numpy as np
from NormalTable import *

#一维分类器：通过区分数值间最大间隔进行递归分类
#使用时需要提前声明2个全局变量：typeList（列表类型），depth（整形）
#输入参数：1为有序列表 2为置信度 3为总样本数
globalDepth = 0
typeList = []
def typeClassifier(sortList,reliability = 0.9,globalcount = 1):
    def maxTap(sortList):
        maxtap = 0.0
        index = 0
        i = 1
        while i < len(sortList):
            chazhi = sortList[i] - sortList[i - 1]
            i += 1
            if chazhi > maxtap:
                index = i - 1
                maxtap = chazhi
        return maxtap, index
    global  typeList, globalDepth
    oldList = sortList.copy()
    total = len(sortList)
    maxtap, index = maxTap(sortList)
    if index == 0 :
        # typeList.append((np.mean(oldList),np.std(oldList)))
        return  typeList
    list1 = oldList[0:index]
    list2 = oldList[index :total]
    max1 = np.max(list1)
    min1 = np.min(list1)
    max2 = np.max(list2)
    min2 = np.min(list2)
    if (max1 == min1 ):
        a = 0
    else:
        a = np.std(list1) / (np.max(list1) - np.min(list1))

    if (max2 == min2 ):
        b = 0
    else:
        b = np.std(list2)/(np.max(list2)-np.min(list2))

    if maxtap > getValueByProbability(reliability) *(a + b):
        list1 = oldList[0:index]
        list2 = oldList[index :total]
        globalDepth += 1
        if globalDepth > 900 or len(sortList)/globalcount < 0.01: return []
        if len(list1) / total > 0.1: typeClassifier(list1,reliability,globalcount)
        if len(list2) / total > 0.1: typeClassifier(list2,reliability,globalcount)
    else:
        typeList.append((np.mean(oldList),np.std(oldList)))
    return typeList