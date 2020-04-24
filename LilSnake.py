from tkinter import *
from random import randint
    
class Snake:
    def __init__(self):
        window = Tk()
        window.title("My Little Snake")

        self.width = 500
        self.height = 500
        self.canvas = Canvas(window, width = self.width,
                             height = self.height)
        self.canvas.pack()

        frame = Frame(window)
        frame.pack()

        self.score = StringVar()
        Label(frame, text = "Score:").pack(side = LEFT)
        Label(frame, textvariable = self.score).pack(side = LEFT) 
    
        frame1 = Frame(window)
        frame1.pack()
        
        Button(frame1, text = "Pause", command = self.pause).grid(row = 1, column = 1)
        Button(frame1, text = "Restart", command = self.initialize).grid(row = 1, column = 2)
        Label(frame1, text = "Speed: ").grid(row = 1, column = 3)
        self.sleepVar = StringVar()
        Label(frame1, textvariable = self.sleepVar).grid(row = 1, column = 4)
        Button(frame1, text = "+", command = self.faster).grid(row = 1, column = 5)
        Button(frame1, text = "-", command = self.slower).grid(row = 1, column = 6)
                       
        self.canvas.bind("<Key>", self.processKeyEvent)
        self.canvas.focus_set()

        self.speedList = [[20, 9], [40, 8], [60, 7], [80, 6], [100, 5],
                          [120, 4], [140, 3], [160, 2], [180, 1]]
        self.increment = 10
        self.food = 2 * [0]
        
        self.initialize()
               
        window.mainloop()

    def initialize(self):
        x = randint(1, 9) * 10
        y = randint(1, 9) * 10
        self.body = [[x, y]]
        if randint(0,1):
            self.dx = self.increment
            self.dy = 0
        else:
            self.dx = 0
            self.dy = self.increment


        self.speedIndex = 4
        self.sleepVar.set(self.speedList[self.speedIndex][1])
        
        self.status = "Run"
        self.isStopped = False

        self.setFood()
        self.animate()
        
    def processKeyEvent(self, event):
        key = event.keysym
        if key == "space":
            self.pause()
        elif key == "Left":
            if self.dy != 0:
                self.dy = 0
                self.dx = -self.increment
        elif key == "Right":
            if self.dy != 0:
                self.dy = 0
                self.dx = self.increment
        elif key == "Down":
            if self.dx != 0:
                self.dx = 0
                self.dy = self.increment
        elif key == "Up":
            if self.dx != 0:
                self.dx = 0
                self.dy = -self.increment

    def pause(self):
        if self.status == "Over": #status = ["Over", "Pause", "Run"]
            self.isStopped = True
        elif self.status == "Pause":
            self.isStopped = False
            self.status = "Run"
            self.animate()
        elif self.status == "Run":
            self.isStopped = True
            self.status = "Pause"
    
    def faster(self):
        if self.speedIndex > 0:
            self.speedIndex -= 1
            self.sleepVar.set(self.speedList[self.speedIndex][1])

    def slower(self):
        if self.speedIndex < len(self.speedList) - 1:
            self.speedIndex += 1
            self.sleepVar.set(self.speedList[self.speedIndex][1])

    def setFood(self):
        self.canvas.delete("food")
        self.food[0] = (randint(20, self.width - 20) // 10) * 10
        self.food[1] = (randint(20, self.height - 20) // 10) * 10
        index = randint(0, 2)
        size = 4
        if index == 0:
            self.foodType = "Bomb"
            color = "black"
        elif index == 1:
            self.foodType = "Food"
            color = "green"
        else:
            self.foodType = "Superfood"
            color = "red"
            size = 6
                
        self.canvas.create_oval(self.food[0] - size, self.food[1] - size,
                                self.food[0] + size, self.food[1] + size,
                                fill = color, outline = color, tags = "food")
        self.isEaten = False
       
    def animate(self):
        count = 0
        while not self.isStopped:
            self.canvas.after(self.speedList[self.speedIndex][0])
            self.canvas.update()
            self.canvas.delete("body")            
            self.redisplayBody()
            if self.foodType == "Bomb":
                if count > 50:
                    self.setFood()
                    count = 0
                else:
                    count += 1
    def getStatus(self, head):
        if head[0] > self.width - 5 or head[0] < 5 \
            or head[1] > self.height - 5 or head[1] < 5:
                self.status = "Over"
                self.pause()

        for i in range(1, len(self.body)):
            if head == self.body[i]:
                self.status = "Over"
                self.pause()
                
    def redisplayBody(self):
        head = [self.body[0][0] + self.dx, self.body[0][1] + self.dy]

        self.getStatus(head)
        
        if head == self.food:
            if self.foodType == "Bomb":
                self.body.pop()
            elif self.foodType == "Superfood":
                self.body.insert(0, head)
                head = [self.body[0][0] + self.dx, self.body[0][1] + self.dy]
                self.body.insert(0, head)
            else:
                self.body.insert(0, head)
            self.setFood()
            
        else:    
            self.body.insert(0, head)
            self.body.pop()
        
        for i in range(1, len(self.body)):
            self.canvas.create_rectangle(self.body[i][0] - 4, self.body[i][1] - 4,
                                         self.body[i][0] + 4, self.body[i][1] + 4,
                                         tags = "body")
        self.canvas.create_oval(head[0] - 4, head[1] - 4,
                                head[0] + 4, head[1] + 4,
                                tags = "body")

        
        self.score.set(len(self.body))

Snake()

#wall last for some time
