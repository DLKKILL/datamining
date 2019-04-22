# -*- coding: utf-8 -*-


"""
由初始数据集生成初始候选集
"""
def createC1(dataSet):
    C1=[]
    for x in dataSet:
        for y in x:
            if y not in C1:
                C1.append(y)
    return list(map(frozenset,C1))


"""
扫描数据集，由候选项集生成符合条件的频繁项集
"""
def scanD(C1,D,miniSupport):
    num = len(D)
    supportMap={}
    freList=[]
    for item in C1:
        for event in D:
            if item.issubset(event):
                if item not in supportMap:
                    supportMap[item]=1
                else:
                    supportMap[item]=supportMap[item]+1
    for key in supportMap:
        t = supportMap[key]/num
        if t >= miniSupport:
            freList.append(key)
        supportMap[key]=t
    return freList,supportMap


"""
生成频繁一项集
"""
def createFreSet(dataSet,miniSupport):
    C1=createC1(dataSet)
    D=list(map(set,dataSet))
    fre1_List,miniSupport=scanD(C1,D,miniSupport)
    return fre1_List,miniSupport


"""
根据支持度对频繁一项集进行排序
返回排序后的频繁项集
"""
def sortFreList(frelist,supportMap):
    freSupportMap={}
    for item in frelist:
        freSupportMap[item]=supportMap[item]
    items=freSupportMap.items()
    tmp=[[v[1],v[0]] for v in items]
    tmp.sort()
    return [tmp[i][1] for i in range(0,len(tmp))]


"""
定义树的节点结果
"""
class TreeNode:
    def __init__(self,name,value,parentNode):
        self.count=value
        self.name=name
        self.linkNode=None
        self.parentNode=parentNode
        self.childNode={}
    def addChildNode(self,name,value):
        self.childNode[name]=value
        self.count=self.count+1
    def getParentNode(self):
        return self.parentNode
    def getCount(self):
        return self.count
    def setLinkNode(self,nextNode):
        self.linkNode=nextNode
    def getLinkNode(self):
        return self.linkNode
    def getChildNode(self):
        return self.childNode

"""
获得某一链表的尾节点
"""
def getLastNode(node):
    t=node
    while(t.getLinkNode!=None):
        t=t.getLinkNode()
    return t


"""
生成初始fp树
"""
def creatFpTree(frelist,supportMap,D):
    head=TreeNode("",0,None)
    headtable={}
    for item in D:
        tmp=head
        for fre in frelist:
            childNodes=tmp.getChildNode()
            if fre in item:
                if fre in childNodes:
                    tmp=childNodes[fre]
                else:
                    node=TreeNode(fre,0,tmp)
                    if fre not in headtable:
                        headtable[fre]=node
                    else:
                        preNode=getLastNode(headtable[fre])
                        preNode.setLinkNode(node)
                    tmp.addChildNode(fre,node)
                    tmp=node
    return head,headtable

"""
fp-growth算法的主函数
"""
def fpGrowth(dataSet,miniSupport):
    freList,supportMap=createFreSet(dataSet,miniSupport)
    sortfrelist=sortFreList(freList,supportMap)
    head,headtable=creatFpTree(sortfrelist,supportMap,dataSet)
if __name__ == "__main__":
    pass
