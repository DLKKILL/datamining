# -*- coding: utf-8 -*-

"""
加载初始数据
"""
def load_data():
    return  [['r','z','h','j','p'],['z','y','x','w','v','u','t','s'],['z'],['r','x','n','o','s'],['y','r','x','z','q','t','p'],['y','z','x','e','q','s','t','m']]

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
        for tmp in D.items():
            event=tmp[0]
            value=tmp[1]
            for i in range(value):
                if item.issubset(event):
                    if item not in supportMap:
                        supportMap[item]=1
                    else:
                        supportMap[item]=supportMap[item]+1
    for key in supportMap:
        #暂时使用最小支持度计数，而不是最小支持度
        t = supportMap[key]
        if t >= miniSupport:
            freList.append(key)
        supportMap[key]=t
    return freList,supportMap


"""
生成频繁一项集
"""
def createFreSet(dataSet,miniSupport):
    C1=createC1(dataSet)
    tmp_dataSet={}
    for item in dataSet:
        tmp_dataSet[item]=1
    dataSet=tmp_dataSet
    D=dataSet
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
    tmp.sort(reverse=True)
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
    def addCount(self):
        self.count=self.count+1
        if self.parentNode != None:
            self.parentNode.addCount()
    def addCountByValue(self,value):
        self.count=self.count+value
        if self.parentNode != None:
            self.parentNode.addCountByValue(value)
"""
获得某一链表的尾节点
"""
def getLastNode(node):
    t=node
    while(t.getLinkNode()!=None):
        t=t.getLinkNode()
    return t


"""
生成初始fp树
"""
def creatFpTree(frelist,supportMap,D):
    treehead=TreeNode("",0,None)
    frelist=list(map(frozenset,frelist))
    headtable={}
    for item in D:
        tmp=treehead
        for fre in frelist:
            childNodes=tmp.getChildNode()
            if fre.issubset(item):
                if fre in childNodes:
                    tmp=childNodes[fre]
                else:
                    fre_name = None
                    for s in fre:
                        fre_name=s
                    node=TreeNode(fre_name,0,tmp)
                    if fre not in headtable:
                        headtable[fre]=node
                    else:
                        preNode=getLastNode(headtable[fre])
                        preNode.setLinkNode(node)
                    tmp.addChildNode(fre,node)
                    tmp=node
        tmp.addCount()
    return treehead,headtable
"""
发现一个节点的前缀节点路径
"""
def getPrePath(node,path):
    if node.name == "":
        return
    path.append(node.name)
    getPrePath(node.getParentNode(),path)
"""
构建条件模式基
"""
def getAllPrePath(headtable,treehead,frelist):
    allPath={}
    for fre in frelist:
        node=headtable[fre]
        allPath[fre]={}
        while(node!=None):
            path=[]
            getPrePath(node.getParentNode(),path)
            path=frozenset(path)
            allPath[fre][path]=node.getCount()
            node=node.getLinkNode()
    return  allPath
"""
获得条件fp树中所有满足最小支持度计数条件的节点
"""
def getAllfre(frelist,miniSupport,headNode):
    if headNode == None:
        return
    if headNode.name != "" and headNode.count >= miniSupport:
        frelist.append(headNode.name)
    for item in headNode.getChildNode():
        getAllfre(frelist,miniSupport,headNode.getChildNode()[item])
"""
构建条件FP树
"""
def createMiniTree(fre,allPath,miniSupport):
    frepathSet=allpath[fre]
    temp_freSet=None
    C1=createC1(frepathSet)
    freList,supportMap=scanD(C1, frepathSet, miniSupport)
    sortfrelist=sortFreList(freList,supportMap)
    headNode=TreeNode("",0,None)
    for item in frepathSet:
        tmp = headNode
        for value in sortfrelist:
            if value.issubset(item):
                childNodes=tmp.getChildNode()
                if value in childNodes:
                    tmp=childNodes[value]
                else:
                    fre_name = None
                    for s in value:
                        fre_name = s
                    node = TreeNode(fre_name, 0, tmp)
                    tmp.addChildNode(value,node)
                    tmp=node
        tmp.addCountByValue(frepathSet[item])
    frelist=[]
    getAllfre(frelist,miniSupport,headNode)
    return frelist
"""
fp-growth算法的主函数
"""
def fpGrowth(dataSet,miniSupport):
    dataSet=list(map(frozenset,dataSet))
    freList,supportMap=createFreSet(dataSet,miniSupport)
    sortfrelist=sortFreList(freList,supportMap)
    treehead,headtable=creatFpTree(sortfrelist,supportMap,dataSet)
    allpath = getAllPrePath(headtable,treehead,sortfrelist)
    return allpath,sortfrelist
if __name__ == "__main__":
    data=load_data()
    allpath,sortfrelist = fpGrowth(data,3)
    ans=[]
    for fre in sortfrelist:
        frelist=createMiniTree(fre,allpath,3)
        ans.append(fre)
        t=[]
        for item in frelist:
            t.append(fre|frozenset(item))
        s=t
        while(True):
            h=[]
            for i in range(len(s)):
                for j in range(i,len(s)):
                    x=(s[i]|s[j])
                    if len(x)==len(s[i])+1 and x not in h:
                        h.append(x)
            if(len(h)==0):
                break
            t.extend(h)
            s=h
        if (len(t) > 0):
            ans.extend(t)
    ans.sort()
    print(ans)

