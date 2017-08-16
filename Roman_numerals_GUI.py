#coding=UTF-8
from Tkinter import *

class App:

    def __init__(self, master):
        self.l1 = Label(master, text="一个优雅的罗马数字转换器<(0^◇^0)>")
        self.l1.grid(row=0,columnspan=3, sticky=W)

        self.l1 = Label(master, text="输入")
        self.l1.grid(row=1)

        self.v = IntVar()
        self.e1 = Entry(master, textvariable=self.v)
        self.e1.grid(row=1, column=1)

        self.b1 = Button(master, text="转换", command=self.convert)
        self.b1.grid(row=1, column=2)

        self.m = StringVar()
        self.m1 = Message(master, textvariable=self.m, aspect=5000)
        self.m1.grid(row=2, columnspan=3, sticky=W)


    def convert(self):
        bd = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII", 8: "VIII", 9: "IX"}
        td = {1: "X", 2: "XX", 3: "XXX", 4: "XL", 5: "L", 6: "LX", 7: "LXX", 8: "LXXX", 9: "XC"}
        hd = {1: "C", 2: "CC", 3: "CCC", 4: "CD", 5: "C", 6: "DC", 7: "DCC", 8: "DCCC", 9: "CM"}
        md = {1: "M", 2: "MM", 3: "MMM"}
        m = ""
        x = self.v.get()
        if x < 0 or x > 3999:
            m = "数字超过范围"
        else:
            if x > 1000:
                m = x / 1000
                m = md.get(m)
                x = x % 1000
            if x > 100:
                h = x / 100
                m = m + hd.get(h)
                x = x % 100
            if x > 10:
                t = x / 10
                m = m + td.get(t)
                x = x % 10
            if x > 0:
                m = m + bd.get(x)
        self.m.set(m)


root = Tk()
app = App(root)
root.mainloop()
