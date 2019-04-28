import operator
from os import listdir

import matplotlib
import matplotlib.pyplot as plt
from numpy import array, shape, tile, zeros


#生成数据
def createDataSet():
    arrays=array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels=['A','A','B','B']
    return arrays,labels

#分类方法
#inx 待分类向量
#dataSet 测试数据
#labels 测试数据标签
#k 取前k个作为样本
def classify(inX,dataSet,labels,k):
    dataSetSize=dataSet.shape[0]
    diffMat=tile(inX,(dataSetSize,1))-dataSet
    sqDiffMat=diffMat**2
    sqDistance=sqDiffMat.sum(axis=1)
    distance=sqDistance**0.5
    index=distance.argsort()
    classCount={}
    for i in range(k):
        lable=labels[index[i]]
        classCount[lable]=classCount.get(lable,0)+1
    #在python3中dict.iteritems()被废弃
    sortedClasssCount=sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    return sortedClasssCount[0][0]

#knn用于约会网站
def file2matrix(filename):
    fr=open(filename)
    datalines=fr.readlines()
    numberoflines=len(datalines)
    returnMat=zeros((numberoflines,3))
    classlabelVector=[]
    index=0
    for line in datalines:
        line=line.strip()
        listfromline=line.split('\t')
        returnMat[index,:]=listfromline[0:3]
        classlabelVector.append(int(listfromline[-1]))
        index=index+1
    return returnMat,classlabelVector

def analydata():
    a,b=file2matrix('datingTestSet2.txt')
    #创建一个图形实例
    fig=plt.figure()
    ax=fig.add_subplot(111)
    #scatter方法创建散点图
    #分析图像可以发现使用第一列和第二列数据特征更加明显
    ax.scatter(a[:,0],a[:,1],15.0*array(b),15.0*array(b))
    plt.show()
analydata() 

#数据归一化处理
def data2normal(dataSet):
    min=dataSet.min(0) #得到的是向量
    max=dataSet.max(0)
    range=max-min
    normalDataSet=zeros(shape(dataSet))
    m=dataSet.shape[0]
    normalDataSet=dataSet-tile(min,(m,1))
    normalDataSet=normalDataSet/tile(range,(m,1))
    return normalDataSet

def datingClassTest():
    hoRatio=0.10
    datingDataMat,datingLables=file2matrix('datingTestSet2.txt')
    normMat=data2normal(datingDataMat)
    m=normMat.shape[0]
    numTestVecs=int(hoRatio*m)
    errorCount=0
    for i in range(numTestVecs):
        result=classify(normMat[i,:],normMat[numTestVecs:m,:],datingLables[numTestVecs:m],3)
        print("the classify come back with: %d,the real answer is: %d"
        %(result,datingLables[i]))
        if(result!=datingLables[i]):
            errorCount+=1.0
    print("error rate is:%f"%(errorCount/float(numTestVecs)))

#datingClassTest()


#knn手写识别系统
#将一张32*32的图片转换成1*1024的向量
def img2vector(filename):
    fr=open(filename)
    returnVect=zeros((1,1024))
    for i in range(32):
        linestr=fr.readline()
        for j in range(32):
            returnVect[0,i*32+j]=int(linestr[j])
    return returnVect

def handwritingClassTest():
    hwlabels=[]
    traingfilelist=listdir('digits/trainingDigits')
    m=len(traingfilelist)
    trainingDataMat=zeros((m,1024))
    for i in range(m):
        filenameStr=traingfilelist[i]
        fileStr=filenameStr.split('.')[0]
        label=int(fileStr.split('_')[0])
        hwlabels.append(label)
        trainingDataMat[i,:]=img2vector
        ('digits/trainingDigits/%s' % filenameStr)
    errorCount=0.0
    testfilelist=listdir('digits/testDigits')
    mTest=len(testfilelist)
    for i in range(mTest):
        filenameStr=testfilelist[i]
        fileStr=filenameStr.split('.')[0]
        label=int(fileStr.split('_')[0])
        testVector=img2vector('digits/testDigits/%s' %filenameStr)
        result=classify(testVector,trainingDataMat,hwlabels,3)
        print('come back with: %d,the real answer is: %d' % (int(result),label))
        if(int(result)!=label):
            errorCount=errorCount+1.0
    print('total number errors is :%f' % errorCount)
    print('error rate is :%f'% (errorCount/float(mTest)))
#handwritingClassTest()