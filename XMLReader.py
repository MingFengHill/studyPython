#encoding=utf-8
from xml.dom import minidom

#全局变量,便于修改
GApath=u"D:\GantryAngle.txt"
XMLpath=u"D:\elektaGeometry.xml"

def TXTCreator(gas):
    global GApath
    f = open(GApath, 'w')
    for i in gas:
            f.write(str(i) + '\n')
    f.close()

def main():
    doc = minidom.parse(XMLpath)
    root = doc.documentElement
    Projections = root.getElementsByTagName("Projection")
    gas = []
    for Projection in Projections:
        ga = Projection.getElementsByTagName("GantryAngle")
        ga = ga[0]
        gas.append(ga.firstChild.data)

    TXTCreator(gas)

main()
