#coding=UTF-8
from Tkinter import *
from random import randint
import tkMessageBox

class Grid(object):
    def __init__(self, master=None,height=16, width=24, offset=10, grid_width=50, bg="#808080"):
        self.height = height
        self.width = width
        self.offset = offset
        self.grid_width = grid_width
        self.bg = bg
        self.canvas = Canvas(master, width=self.width*self.grid_width+2*self.offset, height=self.height*self.grid_width+
                                                                                            2*self.offset, bg=self.bg)
        self.canvas.pack(side=RIGHT, fill=Y)

    def draw(self, pos, color, ):
        x = pos[0] * self.grid_width + self.offset
        y = pos[1] * self.grid_width + self.offset
        #outline属性要与网格的背景色（self.bg）相同，要不然会很丑
        self.canvas.create_rectangle(x, y, x + self.grid_width, y + self.grid_width, fill=color, outline=self.bg)

class Food(object):
    def __init__(self, grid, color = "#23D978"):
        self.grid = grid
        self.color = color
        self.set_pos()
        self.type = 1

    def set_pos(self):
        x = randint(0, self.grid.width - 1)
        y = randint(0, self.grid.height - 1)
        self.pos = (x, y)

    def display(self):
        self.grid.draw(self.pos, self.color)


class Snake(object):
    def __init__(self, grid, color = "#5FA8D9"):
        self.grid = grid
        self.color = color
        self.body = [(8, 11), (8, 12), (8, 13)]
        self.direction = "Up"
        for i in self.body:
            self.grid.draw(i, self.color)

    #这个方法用于游戏重新开始时初始化贪吃蛇的位置
    def initial(self):
        while not len(self.body) == 0:
            pop = self.body.pop()
            self.grid.draw(pop, self.grid.bg)
        self.body = [(8, 11), (8, 12), (8, 13)]
        self.direction = "Up"
        for i in self.body:
            self.grid.draw(i, self.color)

    #蛇像一个指定点移动
    def move(self, new):
        self.body.insert(0, new)
        pop = self.body.pop()
        self.grid.draw(pop, self.grid.bg)
        self.grid.draw(new, self.color)

    #蛇像一个指定点移动，并增加长度
    def add(self ,new):
        self.body.insert(0, new)
        self.grid.draw(new, self.color)

    #蛇吃到了特殊食物1，剪短自身的长度
    def cut_down(self,new):
        self.body.insert(0, new)
        self.grid.draw(new, self.color)
        for i in range(0,3):
            pop = self.body.pop()
            self.grid.draw(pop, self.grid.bg)

    #蛇吃到了特殊食物2，回到最初长度
    def init(self, new):
        self.body.insert(0, new)
        self.grid.draw(new, self.color)
        while len(self.body) > 3:
            pop = self.body.pop()
            self.grid.draw(pop, self.grid.bg)

class SnakeGame(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid = Grid(master)
        self.snake = Snake(self.grid)
        self.food = Food(self.grid)
        self.gameover = False
        self.score = 0
        self.status = ['run', 'stop']
        self.speed = 300
        self.grid.canvas.bind_all("<KeyRelease>", self.key_release)
        self.display_food()
        #界面左侧显示分数
        self.m = StringVar()
        self.ft1 = ('Fixdsys', 40, "bold")
        self.m1 = Message(master, textvariable=self.m, aspect=5000, font=self.ft1, bg="#696969")
        self.m1.pack(side=LEFT, fill=Y)
        self.m.set("Score:"+str(self.score))

    #这个方法用于游戏重新开始时初始化游戏
    def initial(self):
        self.gameover = False
        self.score = 0
        self.m.set("Score:"+str(self.score))
        self.snake.initial()

    def display_food(self):
        self.food.color = "#23D978"
        self.food.type = 1
        if randint(0, 30) == 5:
            self.food.color = "#FFD700"
            self.food.type = 3
            while (self.food.pos in self.snake.body):
                self.food.set_pos()
            self.food.display()
        elif len(self.snake.body) > 10 and randint(0, 8) == 1:
            self.food.color = "#BC8F8F"
            self.food.type = 2
            while (self.food.pos in self.snake.body):
                self.food.set_pos()
            self.food.display()
        else:
            while (self.food.pos in self.snake.body):
                self.food.set_pos()
            self.food.display()

    def key_release(self, event):
        key = event.keysym
        key_dict = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        #蛇不可以像自己的反方向走
        if key_dict.has_key(key) and not key == key_dict[self.snake.direction]:
            self.snake.direction = key
            self.move()
        elif key == 'p':
            self.status.reverse()

    def run(self):
        #首先判断游戏是否暂停
        if not self.status[0] == 'stop':
            #判断游戏是否结束
            if self.gameover == True:
                message = tkMessageBox.showinfo("Game Over", "your score: %d" % self.score)
                if message == 'ok':
                    self.initial()
            self.move()
        self.after(self.speed, self.run)

    def move(self):
        # 计算蛇下一次移动的点
        head = self.snake.body[0]
        if self.snake.direction == 'Up':
            if head[1] - 1 < 0:
                new = (head[0], 16)
            else:
                new = (head[0], head[1] - 1)
        elif self.snake.direction == 'Down':
            new = (head[0], (head[1] + 1) % 16)
        elif self.snake.direction == 'Left':
            if head[0] - 1 < 0:
                new = (24, head[1])
            else:
                new = (head[0] - 1, head[1])
        else:
            new = ((head[0] + 1) % 24, head[1])
            #撞到自己，设置游戏结束的标志位，等待下一循环
        if new in self.snake.body:
            self.gameover=True
        #吃到食物
        elif new == self.food.pos:
            if self.food.type == 1:
                self.snake.add(new)
            elif self.food.type == 2:
                self.snake.cut_down(new)
            else:
                self.snake.init(new)
            self.display_food()
            self.score = self.score+1
            self.m.set("Score:" + str(self.score))
        #什么都没撞到，继续前进
        else:
            self.snake.move(new)

if __name__ == '__main__':
    root = Tk()
    snakegame = SnakeGame(root)
    snakegame.run()
    snakegame.mainloop()