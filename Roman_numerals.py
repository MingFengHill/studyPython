#encoding=utf-8
"""
优雅的阿拉伯数字转化成罗马数字
JeremyWang
"""
#d = {1:1,2:11,3:111,4:12,5:2,6:21,7:211,8:2111,9:13}
bd = {1:"I",2:"II",3:"III",4:"IV",5:"V",6:"VI",7:"VII",8:"VIII",9:"IX"}
td = {1:"X",2:"XX",3:"XXX",4:"XL",5:"L",6:"LX",7:"LXX",8:"LXXX",9:"XC"}
hd = {1:"C",2:"CC",3:"CCC",4:"CD",5:"C",6:"DC",7:"DCC",8:"DCCC",9:"CM"}
md = {1:"M",2:"MM",3:"MMM"}
def Change (x):
    m = ""
    if x>1000:
        m = x/1000
        m = md.get(m)
        x = x%1000
    if x>100:
        h = x/100
        m = m+hd.get(h)
        x = x%100
    if x>10:
        t = x/10
        m = m+td.get(t)
        x= x%10
    if x>0:
        m = m+bd.get(x)
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

