# -*- coding: utf-8 -*-

from functools import reduce

"""
生成初始候选集
输入参数:
Data:初始数据集
返回参数:
返回一个forzenset集合，保护了所有分离出的候选集
"""
def createC1(Data):
    C1=[]
    for event in Data:
        for item in event:
            if [item] not in C1:
                C1.append([item])
    ret=map(frozenset,C1)
    return list(ret)

"""
计算候选集里面的所有候选项哪些符合最小支持度要求
输入参数：
C:候选集
Data:初始数据集
miniSupport:最小支持度
返回参数:
freqList:所有的频繁项集集合
supportMap:所有的候选项集所对应的
"""
def ScanD(C,Data,miniSupport):
    supportMap={}
    num=len(Data)
    freqList=[]
    numberMap=dict()
    for item in Data:
        for c in C:
            if c.issubset(item):
                if c not in numberMap:
                    numberMap[c]=1
                else:
                    numberMap[c]+=1
    for key in numberMap:
        support=numberMap[key]/num
        if support>=miniSupport:
            freqList.append(key)
        supportMap[key]=support
    return freqList,numberMap
"""
aparioriGen函数，根据频繁项集生成新的候选项集
"""
def aparioriGen(LK,k):
    retList=[]
    lenLK=len(LK)
    for i in range(lenLK):
        for j in range(i+1,lenLK):
            L1=list(LK[i])[:k-2]
            L2=list(LK[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1==L2:
                retList.append(LK[i]| LK[j])
    return retList
"""
Apriori算法的主要部分
输入一个初始数据集和最小支持度参数，返回所有的频繁项的集合
输入参数:
    dataSet:初始数据集
    miniSupport:最小支持度参数
返回:
    所有频繁项的集合以及所有项的支持度map
"""
def apriori(dataSet,miniSupport):
    supportMap=dict()
    D=list(map(set,dataSet))
    c1=createC1(D)
    freList,supportValue=ScanD(c1,D,miniSupport)
    supportMap.update(supportValue)
    k=2
    retfreList=[freList]
    while(len(retfreList[k-2])>0):
        CK=aparioriGen(retfreList[k-2],k)
        freList,supportValue=ScanD(CK,D,miniSupport)
        supportMap.update(supportValue)
        retfreList.append(freList)
        k=k+1
    return retfreList,supportMap

def loadDataSet():
    return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]

if __name__ == '__main__':
    dataSet=loadDataSet()
    x,y=apriori(dataSet,0.5)
    print(x)