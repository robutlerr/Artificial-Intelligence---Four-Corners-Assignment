class Problem:
    def __init__ (self, mazeFile):
        self.xStep = 40
        self.yStep = 40
        self.readMaze (mazeFile)

    def readMaze (self, mazeFile):
        self.walls = []
        self.pacman = 0
        self.food = []
        self.xMax = 0
        self.yMax = 0
        
        f = open (mazeFile, 'r')
        if f:
            y = 0
            while True:
                s = list (f.readline ())
                #print (s)
                
                if s == []: break
                if s[-1] == '\n': s.pop()
                x=0
                for k in s:
                    if k == '*': self.walls.append ((x, y))
                    if k == 'P': self.pacman = (x, y)
                    if k == '.': self.food.append ((x, y))
                    x += 1
                y += 1
                self.xMax = max (self.xMax, x)
            self.yMax = y            
            return True
        else:
            print ('File not found')
        return False

    def startState (self):
        return (self.pacman, self.food)

    def isGoal (self, node):
        return node[1] == []

    def transition (self, node):
        x, y = node[0]
        newState = []

        potential_moves = [((x+1, y), 'R'),
                           ((x-1, y), 'L'),
                           ((x, y+1), 'D'),
                           ((x, y-1), 'U')]

        moves = [(move, a) for move, a in potential_moves if 0 <= move[0] < self.xMax and
                 0 <= move[1] < self.yMax and move not in self.walls]
        newStates = []
        
        for k, action in moves:
            remainingDots = node[1].copy()
            if k in remainingDots:
                remainingDots.remove(k)
            newState.append (((k, remainingDots), action, 1))

        return newState

    def compute_distances (self):
        self.dist = {}
        for f in self.food:
            self.dist[(self.pacman, f)] = self.BFS(self.pacman, f)
            for d in self.food:
                if d == f: continue
                plan1 = self.BFS(f, d)
                self.dist[(f, d)] = plan1.copy()
                # reverse plan1:
                plan2=[]
                for k in plan1:
                    if k == 'U': plan2.append('D')
                    if k == 'D': plan2.append('U')
                    if k == 'L': plan2.append('R')
                    if k == 'R': plan2.append('L')
                plan2.reverse()
                self.dist[(d, f)] = plan2

    def BFS(self, start_pos, target_pos):
        def construct_path(node, visited):
            path = []
            while node:
                node, a = visited[node]
                if node != None: path = [a] + path
            return path
        def transition(node):
            x, y = node

            potential_moves = [((x+1, y), 'R'),
                               ((x-1, y), 'L'),
                               ((x, y+1), 'D'),
                               ((x, y-1), 'U')]

            moves = [(move, a) for move, a in potential_moves if 0 <= move[0] < self.xMax and
                     0 <= move[1] < self.yMax and move not in self.walls]
            return moves
        
        frontier = [(start_pos, None, None)]
        visited = {}
        while frontier:
            node, parent, action = frontier.pop(0)
            if node in visited: continue
            visited[node] = (parent, action)
            if node == target_pos: return construct_path(node, visited)
            neighbors = transition(node)
            for n, a in neighbors:
                frontier.append ((n, node, a))
        return None
                

    def nextStates(self, node):
        # method to return the next state with the cost.
        # Return value is a tuple of the form:
        #   (cost, (pacman_pos, remaining_dots), actions)
        # The actions are the plan to move from pacman_pos to one
        # of the dot in the remaining_dots
        neighbors = []
        for f in node[1]:
            #plan = self.BFS(node[0], f)
            
            plan = self.dist[(node[0], f)]
            dots = node[1].copy()
            dots.remove(f)
            #neighbors.append ((len(plan), (f, dots), plan))
            neighbors.append ((len(plan), (f, dots), plan))
        return neighbors 

    def h(self, state):
        # heuristic method that computes the minimum manhattan distance
        # from pacman position to every remaining dot.

        # starting pacman position (4,2)
        # locations of the foods [(1, 1), (6, 1), (1, 6), (6, 6)]

        
        # getting the positions from the state passed into the function
        pacman_pos, remaining_dots = state
        if not remaining_dots:
            return 0
        # accumulator
        sumSteps = 0
        # define and set each mst to false for every food item
        mst = {f: False for f in remaining_dots}
        # set the current position to where pacman is currently located
        currentPosition = pacman_pos

        # loop until all mst values are true (true == food has been reached and completed)
        while not all(mst.values()):
            pacman_pos = currentPosition
            # initializing the minimum food value to none and the initial step value to a number that will be greater than the beginning distance
            minFood = None
            minSteps = float('inf')
            for food in remaining_dots:
                # if mst is false, it will check the value, if not it will skip
                if not mst[food]:
                    # gets the number of steps between pacman and the position
                    steps = self.BFS(currentPosition, food)
                    if isinstance(steps, list):
                        stepCounter = len(steps)
                    else:
                        stepCounter = steps
                    # if it is the lowest, it will be set to the lowest
                    if stepCounter < minSteps:
                        minSteps = stepCounter
                        minFood = food
            # pacman's new position is at the food he just "ate"
            currentPosition = minFood
            # incrementing the number of steps calculated to the overall steps
            sumSteps += minSteps
            # sets the food found to have the minimum distance to True so it will not be recalculated
            mst[minFood] = True

        # returns the final number of steps (lowest amount) to reach all four food
        return sumSteps
        
