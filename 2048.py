#coding=UTF-8
from Tkinter import *
from random import randint
from random import choice
import tkMessageBox

"""
When you use python 3.X,you need to use the following header file.

from tkinter import *
from random import randint
from random import choice
import tkinter.messagebox

Author:Jeremy Wang

"""

class Grid(object):
    def __init__(self, master=None, height=4, width=4, offset=10, grid_width=200, bg="#696969"):
        self.height = height
        self.width = width
        self.offset = offset
        self.grid_width = grid_width
        self.bg = bg
        self.canvas = Canvas(master, width=self.width*self.grid_width + 2*self.offset,height=self.height*self.grid_width+2*self.offset, bg=self.bg)
        self.initial()

    def initial(self):
        for i in range(0,4):
            for j in range(0,4):
                x = i * self.grid_width + self.offset
                y = j * self.grid_width + self.offset
                self.canvas.create_rectangle(x+10, y+10, x + self.grid_width-10, y + self.grid_width-10, fill="#808080",outline=self.bg)
        self.canvas.pack(side=RIGHT, fill=Y)

    def draw(self, pos, color, text):
        x = pos[0] * self.grid_width + self.offset
        y = pos[1] * self.grid_width + self.offset
        # outline属性要与网格的背景色（self.bg）相同，要不然会很丑
        self.canvas.create_rectangle(x+10, y+10, x + self.grid_width-10, y + self.grid_width-10, fill=color, outline=self.bg)
        ft1 = ('Comic Sans MS', 50, "bold")
        self.canvas.create_text(pos[0] * 200 + 110, pos[1] * 200 + 110, text=text, font=ft1)


class Matrix(object):
    def __init__(self, grid):
        self.grid = grid
        self.matrix = [[0 for i in range(4)] for i in range(4)]
        self.matrix_o = [[0 for i in range(4)] for i in range(4)]
        self.vacancy = []
        self.gamewin = False
        #使用一个字典将数字与其对应的颜色存放起来
        self.color ={0:"#808080", 2:"#FFFACD", 4:"#F5DEB3", 8:"#F0E68C", 16:"#FFFF00", 32:"#FFD700", 64:"#FFA500", 128:"#FF8C00",
                     256:"#CD5C5C", 512:"#FF6347", 1024:"#FF0000", 2048:"#00FFFF"}

    def initial(self):
        self.matrix = [[0 for i in range(4)] for i in range(4)]
        self.void()
        self.generate()
        self.generate()
        self.draw()
	self.gamewin = False
        for i in range(0, 4):
            for j in range(0, 4):
                self.matrix_o[i][j] = self.matrix[i][j]



    def draw(self):
        for i in range (0, 4):
            for j in range (0, 4):
                pos = (i, j)
                text = str(self.matrix[i][j])
                color = self.color[self.matrix[i][j]]
                self.grid.draw(pos, color, text)

    #计算空位
    def void(self):
        self.vacancy = []
        for x in range(0,4):
            for y in range(0,4):
                if self.matrix[x][y] == 0:
                    self.vacancy.append((x,y))
        return len(self.vacancy)

    #在空位中，随机生成2或4
    def generate(self):
        pos=choice(self.vacancy)
        if randint(0,5)==4:
            self.matrix[pos[0]][pos[1]] = 4
        else:
            self.matrix[pos[0]][pos[1]] = 2
        del self.vacancy[self.vacancy.index((pos[0], pos[1]))]

    #矩阵左移
    def up(self):
        ss = 0
        for i in range(0, 4):
            for j in range(0, 3):
                s = 0
                if not self.matrix[i][j] == 0:
                    for k in range(j + 1, 4):
                        if not self.matrix[i][k] == 0:
                            if self.matrix[i][j] == self.matrix[i][k]:
                                ss = ss + self.matrix[i][k]
                                self.matrix[i][j] = self.matrix[i][j] * 2
                                if self.matrix[i][j] == 2048:
                                    self.gamewin = True
                                self.matrix[i][k] = 0
                                s = 1
                                break
                            else:
                                break
                    if s == 1:
                        break
        for i in range(0, 4):
            s = 0
            for j in range(0, 3):
                if self.matrix[i][j - s] == 0:
                    self.matrix[i].pop(j - s)
                    self.matrix[i].append(0)
                    s = s + 1
        return ss

    #矩阵右移
    def down(self):
        for i in range(0, 4):
            self.matrix[i].reverse()
        ss = self.up()
        for i in range(0, 4):
            self.matrix[i].reverse()
        return ss

    #矩阵上移
    def left(self):
        ss = 0
        for i in range(0, 4):
            for j in range(0, 3):
                s = 0
                if not self.matrix[j][i] == 0:
                    for k in range(j + 1, 4):
                        if not self.matrix[k][i] == 0:
                            if self.matrix[j][i] == self.matrix[k][i]:
                                ss = ss + self.matrix[k][i]
                                self.matrix[j][i] = self.matrix[j][i] * 2
                                if self.matrix[j][i] == 2048:
                                    self.gamewin = True
                                self.matrix[k][i] = 0
                                s = 1
                                break
                            else:
                                break
                    if s == 1:
                        break
        for i in range(0, 4):
            s = 0
            for j in range(0, 3):
                if self.matrix[j-s][i] == 0:
                    for k in range(j-s, 3):
                        self.matrix[k][i] = self.matrix[k+1][i]
                    self.matrix[3][i] = 0
                    s = s+1
        return ss

    #矩阵下移
    def right(self):
        ss = 0
        for i in range(0, 4):
            for j in range(0, 3):
                s = 0
                if not self.matrix[3-j][i] == 0:
                    k = 3-j-1
                    while k >= 0:
                        if not self.matrix[k][i] == 0:
                            if self.matrix[3-j][i] == self.matrix[k][i]:
                                ss = ss +  self.matrix[k][i]
                                self.matrix[3-j][i] = self.matrix[3-j][i] * 2
                                if self.matrix[3-j][i] == 2048:
                                    self.gamewin = True
                                self.matrix[k][i] = 0
                                s = s+1
                                break
                            else:
                                break
                        k = k -1
                if s == 1:
                        break
        for i in range(0, 4):
            s = 0
            for j in range(0, 3):
                if self.matrix[3-j+s][i] == 0:
                    k = 3-j+s
                    while k > 0:
                        self.matrix[k][i] = self.matrix[k-1][i]
                        k = k-1
                    self.matrix[0][i] = 0
                    s = s+1
        return ss

class Game(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid = Grid(master)
        self.matrix = Matrix(self.grid)
        self.score = 0
        self.status = ['run', 'stop']
        self.grid.canvas.bind_all("<KeyRelease>", self.key_release)

        #界面左侧显示分数
        self.m = StringVar()
        self.ft1 = ('Times New Roman', 40, "bold")
        self.m1 = Message(master, textvariable=self.m, aspect=5000, font=self.ft1, bg="#696969")
        self.m1.pack(side=LEFT, fill=Y)
        self.m.set("Score:"+str(self.score))

        self.initial()

    #这个方法用于游戏重新开始时初始化游戏
    def initial(self):
        self.score = 0
        self.m.set("Score:"+str(self.score))
        self.matrix.initial()

    def key_release(self, event):
        key = event.keysym
        if key == "Up":
            ss = self.matrix.up()
            self.run(ss)
        elif key == "Down":
            ss = self.matrix.down()
            self.run(ss)
        elif key == "Left":
            ss = self.matrix.left()
            self.run(ss)
        elif key == "Right":
            ss = self.matrix.right()
            self.run(ss)

    def run(self, ss):
        if not self.matrix.matrix == self.matrix.matrix_o:
            self.score = self.score + int(ss)
            self.m.set("Score:" + str(self.score))
            if self.matrix.gamewin == True:
                self.matrix.draw()
                message = tkMessageBox.showinfo("大吉大利，今晚吃鸡！", "你的分数: %d" % self.score)
                if message == 'ok':
                    self.initial()
            else:
                self.matrix.void()
                self.matrix.generate()
                for i in range(0, 4):
                    for j in range(0, 4):
                        self.matrix.matrix_o[i][j] = self.matrix.matrix[i][j]
                self.matrix.draw()
        else:
            v = self.matrix.void()
            if v < 1:
                message = tkMessageBox.showinfo("你输了/(ㄒoㄒ)/~~", "你的分数: %d" % self.score)
                if message == 'ok':
                    self.initial()



if __name__ == '__main__':
    root = Tk()
    game = Game(root)
    game.mainloop()
