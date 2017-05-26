#encoding=utf-8
import re

"""
优雅的阿拉伯数字转化成罗马数字
JeremyWang
"""
d = {1:"1",2:"11",3:"111",4:"12",5:"2",6:"21",7:"211",8:"2111",9:"13"}

def Change (x):
    m = ""
    if x>1000:
        m = x/1000
        m = d.get(m)
        m = re.sub('1','M',m)
        x = x%1000
    if x>100:
        h = x/100
        h = d.get(h)
        h = re.sub('1','C',h)
        h = re.sub('2','D',h)
        h = re.sub('3','M',h)
        m = m + h
        x = x%100
    if x>10:
        t = x/10
        t = d.get(t)
        t = re.sub('1','X',t)
        t = re.sub('2','L',t)
        t = re.sub('3','C',t)
        m = m + t
        x= x%10
    if x>0:
        b = d.get(x)
        b = re.sub('1','I',b)
        b = re.sub('2','V',b)
        b = re.sub('3','X',b)
        m = m + b
    print(m)
def main ():
    print("一个优雅的罗马数字转换器<(0^◇^0)> ")
    while 1:
        x = input("请输入你要转换的数字：")
        if x==quit:
            print("See you.")
            break
        elif x<0 or x>3999:
            print("输出数字超过转换范围")
        else:
            print("转换后的数字是：")
            Change(x)
main()

