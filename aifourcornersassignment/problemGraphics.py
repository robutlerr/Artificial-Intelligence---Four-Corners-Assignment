from graphics import Window
class pacmanGraphic(Window):
    xStep = 40
    yStep = 40
    def gCoord (self, x, y):
        return x*pacmanGraphic.xStep + 10, y*pacmanGraphic.yStep + 10
    
    def drawPacman(self, p, pos):
        x, y = self.gCoord(pos[0], pos[1])
        
        xEye = x + pacmanGraphic.xStep / 2
        yEye = y + pacmanGraphic.yStep / 4
        
        self.pacman = self.arc(x+3, y+3,
                               x+pacmanGraphic.xStep-2,
                               y+pacmanGraphic.yStep-2,
                          startAngle=25, endAngle=315,
                          outline="#000", fill="#ffff00",
                          width=2)
        
        self.pacmanEye =  self.oval(xEye, yEye, xEye+3, yEye+3,
                          fill="#000", width=0.1)

    def drawFood(self, p):
        self.food = []
        for (x, y) in p.food:
            c, r = self.gCoord(x, y)
            
            self.food.append (self.oval(c, r,
                            c+pacmanGraphic.xStep-10,
                            r+pacmanGraphic.yStep-10,
                            fill = '#ffff00',
                            width=0.1))
            
    def addText(self, x, y, str, color='blue'):
        x, y = gCoord(x, y)
        return self.text(x, y, str, color)
    
    def setup(self, p):
        
        for x, y in p.walls:
            c, r = self.gCoord(x, y)
            
            self.rec(c, r, c+pacmanGraphic.xStep,
                     r+pacmanGraphic.yStep,
                     outline='#000',
                     fill='#fff',
                     width=2)
        self.drawFood(p)
        self.drawPacman(p, p.pacman)
        
        #x, y = self.gCoord(p.xMax-1, p.yMax-1)
        #print('text: ', x, y, p.xMax, p.yMax)
        #self.text(x, y, 'Score = 0')

        self.refresh()

    def move_pacman(self, p, pos, action):
        deltaX, deltaY = 0, 0
        if action == 'R': deltaX = 1
        elif action == 'L': deltaX = -1
        if action == 'D': deltaY = 1
        elif action == 'U': deltaY = -1
        
        dx, dy = deltaX * pacmanGraphic.xStep, deltaY * pacmanGraphic.yStep
        self.move(self.pacman, dx, dy)
        self.move(self.pacmanEye, dx, dy)
        x1, y1 = pos
        x1, y1 = x1 + deltaX, y1 + deltaY
        if (x1, y1) in p.food:
            index = p.food.index ((x1, y1))            
            self.remove(self.food[index])
            self.food.pop(index)
            p.food.remove((x1, y1))
        self.refresh()
        self.wait(0.1)

        return x1, y1
        

    def runPlan(self, p, plan):
        x1, y1 = p.pacman
        count = 0
        for action in plan:
            count += 1
            x1, y1 = self.move_pacman (p, (x1, y1), action)

        print('count=', count)

