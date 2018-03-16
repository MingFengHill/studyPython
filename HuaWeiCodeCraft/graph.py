#coding=UTF-8
import matplotlib.pyplot as plt

#全局变量
txtPath = r'C:\Users\Jeremy\Desktop\初赛文档\用例示例\TrainData_2015.1.1_2015.2.19.txt'

#从数据中找到有多少个不同的时间，放到一个list中
time = []
tmp = " "
#第一次读取文件，目的是找到文件中记录来多少天的数据
for line in open(txtPath):
    a,b,c,d = [i for i in line.split()]
    if c!=tmp:
        time.append(c)
        tmp = c
print(time)
#用于保存每一天售出总销量的数组
sum = [0]*len(time)
#用于保存每一种产品销量的数组
flavor1 = [0]*len(time)
flavor2 = [0]*len(time)
flavor3 = [0]*len(time)
flavor4 = [0]*len(time)
flavor6 = [0]*len(time)
flavor5 = [0]*len(time)
flavor7 = [0]*len(time)
flavor8 = [0]*len(time)
flavor9 = [0]*len(time)
flavor10 = [0]*len(time)
flavor11 = [0]*len(time)
flavor12 = [0]*len(time)
flavor13 = [0]*len(time)
flavor14 = [0]*len(time)
flavor15 = [0]*len(time)
#使用hash来做字符串到数组的匹配
dict = {'flavor1':flavor1,'flavor2':flavor2,'flavor3':flavor3,'flavor4':flavor4,
     'flavor5':flavor5,'flavor6':flavor6,'flavor7':flavor7,'flavor8':flavor8
    , 'flavor9': flavor9,'flavor10':flavor10,'flavor11':flavor11,'flavor12':flavor12,
     'flavor13':flavor13,'flavor14':flavor14,'flavor15':flavor15}
#第二次读取文件记录每种产品的销量和总销量
for line in open(txtPath):
    a,b,c,d = [i for i in line.split()]
    index = time.index(c)
    sum[index] = sum[index] + 1
    if b in dict:
        dict[b][index] = dict[b][index]+1

x = [n for n in range(1, len(time)+1)]
#控制折线图x,y轴的长短
plt.figure(figsize=(15, 5))
plt.xlabel('time')
plt.ylabel('number')
plt.plot(x, flavor4, 'r', label='flavor4')
plt.plot(x, flavor9, 'b', label='flavor9')
plt.plot(x, sum, 'g', label='sum')
plt.xticks(x, x, rotation=0)
plt.legend(bbox_to_anchor=[0.3, 1])
plt.grid()
plt.show()