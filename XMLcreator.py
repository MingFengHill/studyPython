#encoding=utf-8
import numpy as np
import math
from xml.dom.minidom import Document

#全局变量,便于修改
GApath=u"D:\GantryAngle.txt"
XMLpath=u"D:\RTKThreeDCircularGeometry.xml"
InPlaneAngle = 0
OutOfPlaneAngle = 0
SourceOffsetX = 0
SourceOffsetY = 0
ProjectionOffsetX = -117.056831359863
ProjectionOffsetY = -1.01187002658844
SourceToDetectorDistance = 1536
SourceToIsocenterDistance = 1000

#从txt文档读取GantryAngle
def GantryAngleReader ():
    global GApath
    result=[]
    f=open(GApath)
    for line in f.readlines():
        result.append(list(map(float, line.split(','))))
    return result

#根据GantryAngle计算所需的矩阵,并把矩阵转化成可以直接输出的形式
def MatrixCreator (ga):
    global InPlaneAngle
    global OutOfPlaneAngle
    global SourceOffsetX
    global SourceOffsetY
    global ProjectionOffsetX
    global ProjectionOffsetY
    global SourceToDetectorDistance
    global SourceToIsocenterDistance
    #按照要求进行矩阵运算
    a = np.matrix([[math.cos(math.radians(-InPlaneAngle)),-math.sin(math.radians(-InPlaneAngle)),0,0],
                   [math.sin(math.radians(-InPlaneAngle)),math.cos(math.radians(-InPlaneAngle)),0,0],
                   [0,0,1,0],
                   [0,0,0,1]])
    b = np.matrix([[1,0,0,0],
                   [0,math.cos(math.radians(-OutOfPlaneAngle)),-math.sin(math.radians(-OutOfPlaneAngle)),0],
                   [0,math.sin(math.radians(-OutOfPlaneAngle)),math.cos(math.radians(-OutOfPlaneAngle)),0],
                   [0,0,0,1]])
    c = np.matrix([[math.cos(math.radians(ga)),0,-(math.sin(math.radians(ga))),0],
                   [0,1,0,0],
                   [math.sin(math.radians(ga)),0,math.cos(math.radians(ga)),0],
                   [0,0,0,1]])
    print(c)
    print(c)
    Mr=a*b*c
    e = np.matrix([[1,0,SourceOffsetX-ProjectionOffsetX],
                   [0,1,SourceOffsetY-ProjectionOffsetY],
                   [0,0,1]])
    d = np.matrix([[-SourceToDetectorDistance,0,0,0],
                   [0,-SourceToDetectorDistance,0,0],
                   [0,0,1,-SourceToIsocenterDistance]])
    f = np.matrix([[1,0,0,-SourceOffsetX],
                   [0,1,0,-SourceOffsetY],
                   [0,0,1,0],
                   [0,0,0,1]])
    m=e*d*f*Mr
    #将计算得到的矩阵整形成需要格式的字符串
    mm=m.tolist()
    st='\n'
    s=0
    for i in mm:
        st=st+'\t\t\t\t'
        s=s+1
        for j in i:
            st=st+str(j)+'\000'
        if s==3:
            st=st+'\n\t\t'
        else:
            st=st+'\n'
    return st

def main ():
    global SourceToDetectorDistance
    global SourceToIsocenterDistance
    global ProjectionOffsetX
    global ProjectionOffsetY

#读取txt中的GantryAng
    GantryAngs=GantryAngleReader()

#输出指定格式的XML
    doc = Document()
    root = doc.createElement('RTKThreeDCircularGeometry')
    root.setAttribute('version', '0')
    doc.appendChild(root)
    nodeSTD = doc.createElement('SourceToIsocenterDistance')
    nodeSTD.appendChild(doc.createTextNode(str(SourceToIsocenterDistance)))
    nodeTDD = doc.createElement('SourceToDetectorDistance')
    nodeTDD.appendChild(doc.createTextNode(str(SourceToDetectorDistance)))
    root.appendChild(nodeSTD)
    root.appendChild(nodeTDD)
    for GantryAng in GantryAngs:
        for ga in GantryAng:
            nodePro = doc.createElement('Projection')
            nodeGA = doc.createElement('GantryAngle')
            nodeGA.appendChild(doc.createTextNode(str(ga)))
            nodePOX = doc.createElement('ProjectionOffsetX')
            nodePOX.appendChild(doc.createTextNode(str(ProjectionOffsetX)))
            nodePOY = doc.createElement('ProjectionOffsetY')
            nodePOY.appendChild(doc.createTextNode(str(ProjectionOffsetY)))
            nodeMatrix = doc.createElement('Matrix')
            nodeMatrix.appendChild(doc.createTextNode(str(MatrixCreator(ga))))
            nodePro.appendChild(nodeGA)
            nodePro.appendChild(nodePOX)
            nodePro.appendChild(nodePOY)
            nodePro.appendChild(nodeMatrix)
            root.appendChild(nodePro)
    fp = open(XMLpath,'w')
    doc.writexml(fp,addindent='\t', newl='\n')
    fp.close()

main()