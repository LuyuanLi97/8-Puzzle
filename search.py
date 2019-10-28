import numpy as np
from PuzzleNode import *
import copy
import time
from queue import PriorityQueue
from itertools import count

def greedySearch(startNode):
    priQueue = PriorityQueue()
    unique = count()
    priQueue.put((startNode.manhattanDist(), next(unique), [startNode, 0]))
    visited = []
    while not priQueue.empty():
        first = priQueue.get()
        nearest = first[2][0]
        step = first[2][1]
        if nearest.isGoal():
            trace = []
            ptr = nearest
            while ptr is not None:
                trace.append(ptr.node)
                ptr = ptr.parent
            return step, trace

        visited.append(nearest)
        validMoves = nearest.getValidMoves()
        for moveChar in validMoves:
            nextNode = copy.deepcopy(nearest)
            nextNode.doMove(moveChar)
            if not inNodeList(nextNode, visited):
                priQueue.put((nextNode.manhattanDist(), next(unique), [nextNode, step+1]))
                nextNode.parent = nearest


def AStarSearch(startNode):
    priQueue = PriorityQueue()
    unique = count()
    priQueue.put((startNode.manhattanDist(), next(unique), [startNode, 0]))
    visited = []
    while not priQueue.empty():
        first = priQueue.get()
        nearest = first[2][0]
        step = first[2][1]
        if nearest.isGoal():
            trace = []
            ptr = nearest
            while ptr is not None:
                trace.append(ptr.node)
                ptr = ptr.parent
            return step, trace

        visited.append(nearest)
        validMoves = nearest.getValidMoves()
        for moveChar in validMoves:
            nextNode = copy.deepcopy(nearest)
            nextNode.doMove(moveChar)
            if not inNodeList(nextNode, visited):
                priQueue.put((nextNode.manhattanDist() + step + 1, next(unique), [nextNode, step + 1]))
                nextNode.parent = nearest


def iterativeDeepeningSearch(startNode):
    maxLayer = 1
    while True:
        dfsList = []
        layer = 0
        dfsList.append((startNode, layer))

        while len(dfsList) != 0:
            top = dfsList.pop()
            tmpNode = top[0]
            tmpLayer = top[1]
            if tmpNode.isGoal():
                trace = []
                ptr = tmpNode
                while ptr is not None:
                    trace.append(ptr.node)
                    ptr = ptr.parent
                return tmpLayer, trace

            nextLayer = tmpLayer + 1
            if nextLayer > maxLayer:
                continue

            validMoves = tmpNode.getValidMoves()
            for moveChar in validMoves:
                nextNode = copy.deepcopy(tmpNode)
                nextNode.doMove(moveChar)
                if not inDFSNodeList(nextNode, dfsList):
                    dfsList.append((nextNode, nextLayer))
                    nextNode.parent = tmpNode
        maxLayer += 1


# check if tNode is in nList (used in iterativeDeepeningSearch())
# nList is a list of tuple (puzzleNode, layer)
def inDFSNodeList(tNode, nList):
    for node in nList:
        if (node[0].node == tNode.node).all():
            return True
    return False

# check is tNode is in nList (used in AStarSearch() and greedySearch())
# nList is a list of PuzzleNode
def inNodeList(tNode, nList):
    for node in nList:
        if (node.node == tNode.node).all():
            return True
    return False

# test average execution time of 20 randomly generated samples
def testIDS():
    totaltime = 0
    print('Testing IDS:')
    for i in range(20):
        print('sample ' + str(i))
        test = PuzzleNode()
        test.shuffle()
        test.show()
        start = time.time()
        step, _ = iterativeDeepeningSearch(test)
        end = time.time()
        print(step)
        totaltime += (end - start)
    avg = totaltime / 20
    print(avg)


def testGreedy():
    totaltime = 0
    print('Testing greedy search:')
    print('Huristic function: Manhattan Distance')
    for i in range(20):
        print('sample' + str(i))
        test = PuzzleNode()
        test.shuffle()
        test.show()
        start = time.time()
        step, _ = greedySearch(test)
        end = time.time()
        print(step)
        totaltime += (end - start)
    avg = totaltime / 20
    print(avg)


def testAStar():
    totaltime = 0
    print('Testing A* search:')
    print('Huristic function: Num of wrong tiles')
    for i in range(20):
        print('sample' + str(i))
        test = PuzzleNode()
        test.shuffle()
        test.show()
        start = time.time()
        step, _ = AStarSearch(test)
        end = time.time()
        print(step)
        totaltime += (end - start)
    avg = totaltime / 20
    print(avg)


# print solution trace
test = PuzzleNode()
test.shuffle()
test.show()
step, trace = iterativeDeepeningSearch(test)
print(step)
while len(trace) != 0:
    n = trace.pop()
    print(n)
