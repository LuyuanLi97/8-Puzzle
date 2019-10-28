import numpy as np

class PuzzleNode:
    def __init__(self, init=None):
        self.goal = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
        self.node = self.goal.copy() if init is None else init.copy()
        self.i0 = 2
        self.j0 = 2
        if init is not None:
            for i in range(3):
                for j in range(3):
                    if self.node[i][j] == 0:
                        self.i0 = i
                        self.j0 = j
        self.parent = None

    def down(self):
        assert self.i0 > 0
        i0 = self.i0
        j0 = self.j0
        self.node[i0][j0], self.node[i0 - 1][j0] = self.node[i0 - 1][j0], self.node[i0][j0]
        self.i0 -= 1

    def up(self):
        assert self.i0 < 2
        i0 = self.i0
        j0 = self.j0
        self.node[i0][j0], self.node[i0 + 1][j0] = self.node[i0 + 1][j0], self.node[i0][j0]
        self.i0 += 1

    def right(self):
        assert self.j0 > 0
        i0 = self.i0
        j0 = self.j0
        self.node[i0][j0], self.node[i0][j0 - 1] = self.node[i0][j0 - 1], self.node[i0][j0]
        self.j0 -= 1

    def left(self):
        assert self.j0 < 2
        i0 = self.i0
        j0 = self.j0
        self.node[i0][j0], self.node[i0][j0 + 1] = self.node[i0][j0 + 1], self.node[i0][j0]
        self.j0 += 1

    def getValidMoves(self):
        validDir = []

        if self.i0 > 0:
            validDir.append('d')
        if self.i0 < 2:
            validDir.append('u')
        if self.j0 > 0:
            validDir.append('r')
        if self.j0 < 2:
            validDir.append('l')
        return validDir

    def doMove(self, moveChar):
        if moveChar == 'd':
            self.down()
        elif moveChar == 'u':
            self.up()
        elif moveChar == 'r':
            self.right()
        elif moveChar == 'l':
            self.left()

    def randomStep(self):
        validDir = self.getValidMoves()

        dirNum = len(validDir)
        randomDir = validDir[np.random.randint(0, dirNum)]
        self.doMove(randomDir)

    def shuffle(self, shuffleTime=20):
        for i in range(shuffleTime):
            self.randomStep()

    def isGoal(self):
        return (self.node == self.goal).all()

    def numOfWrong(self):
        return 9 - np.sum(self.node == self.goal)

    def manhattanDist(self):
        dist = 0
        for i in range(3):
            for j in range(3):
                num = self.node[i][j]
                if num != 0:
                    iGoal = (num - 1) // 3
                    jGoal = (num - 1) % 3
                    dist += abs(iGoal - i) + abs(jGoal - j)
        return dist

    def show(self):
        print(self.node)