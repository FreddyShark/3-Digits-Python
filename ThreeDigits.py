import sys
import random
import queue
from collections import deque
import dataclasses
from dataclasses import dataclass, field
from typing import Any

@dataclass(order=True)
class nodeHwrap:
    h: int
    order: int
    node: Any=field(compare=False)

    def __init__(self, h, order, node):
        self.h = h
        self.order= order
        self.node = node



class node:

    def __init__(self, seq, posChanged = "", parent = None):
        self.seq = seq
        self.posChanged = posChanged
        if parent is not None:
            self.parentSeq = parent.seq
            self.path = parent.path + "," + self.seq
            self.depth = parent.depth + 1
        else:
            self.path = seq
            self.depth = 0
        self.children = []

    def __eq__(self, node):
        if self is None or node is None:
            return False
        if self.seq != node.seq:
            return False
        if len(self.children) != len(node.children):
            return False
        for i in range(len(self.children)):
            if self.children[i].seq != node.children[i].seq:
                return False
        return True

    def __ne__(self, node):
        if self is None or node is None:
            return True
        if self.seq != node.seq:
            return True
        if len(self.children) != len(node.children):
            return True
        for i in range(len(self.children)):
            if self.children[i].seq != node.children[i].seq:
                return True
        return False

    def __hash__(self):
        ID = self.seq
        for child in self.children:
            ID += child.seq
        return int(ID)

    def addChild(self, child):
        self.children.append(child)

    def generateChildren(self):
        if self.posChanged == "L":
            # mid
            if int(self.seq[1]) != 0:
                seq = self.seq[0] + str(int(self.seq[1])-1) + self.seq[2]
                child = node(seq, "M", self)
                self.addChild(child)
            if int(self.seq[1]) != 9:
                seq = self.seq[0] + str(int(self.seq[1])+1) + self.seq[2]
                child = node(seq, "M", self)
                self.addChild(child)
            # right
            if int(self.seq[2]) != 0:
                seq = self.seq[:2] + str(int(self.seq[2])-1)
                child = node(seq, "R", self)
                self.addChild(child)
            if int(self.seq[2]) != 9:
                seq = self.seq[:2] + str(int(self.seq[2])+1)
                child = node(seq, "R", self)
                self.addChild(child)
        elif self.posChanged == "M":
            # left
            if int(self.seq[0]) != 0:
                seq = str(int(self.seq[0])-1) + self.seq[1:]
                child = node(seq, "L", self)
                self.addChild(child)
            if int(self.seq[0]) != 9:
                seq = str(int(self.seq[0])+1) + self.seq[1:]
                child = node(seq, "L", self)
                self.addChild(child)
            # right
            if int(self.seq[2]) != 0:
                seq = self.seq[:2] + str(int(self.seq[2])-1)
                child = node(seq, "R", self)
                self.addChild(child)
            if int(self.seq[2]) != 9:
                seq = self.seq[:2] + str(int(self.seq[2])+1)
                child = node(seq, "R", self)
                self.addChild(child)
        elif self.posChanged == "R":
            # left
            if int(self.seq[0]) != 0:
                seq = str(int(self.seq[0])-1) + self.seq[1:]
                child = node(seq, "L", self)
                self.addChild(child)
            if int(self.seq[0]) != 9:
                seq = str(int(self.seq[0])+1) + self.seq[1:]
                child = node(seq, "L", self)
                self.addChild(child)
            # mid
            if int(self.seq[1]) != 0:
                seq = self.seq[0] + str(int(self.seq[1])-1) + self.seq[2]
                child = node(seq, "M", self)
                self.addChild(child)
            if int(self.seq[1]) != 9:
                seq = self.seq[0] + str(int(self.seq[1])+1) + self.seq[2]
                child = node(seq, "M", self)
                self.addChild(child)



def BFS(fileName):
    start, goal, forbiddens = readFile(fileName)

    if start == goal:
        print (start)
        print (start)
        return
    
    root = getFirstLevelStates(start)
    visited = set()
    visited.add(root)

    fringe = queue.Queue()
    expanded = root.seq

    # create fringe
    for child in root.children:
        if not child.seq in forbiddens:
            fringe.put(child)
    i = 1
    while i < 1000:

        if fringe.empty():
            break
        # get next node in fringe
        visiting = fringe.get()
        # generate children
        visiting.generateChildren()

        # check for originality. move to next node if not original
        if visiting in visited or visiting.seq in forbiddens:
            continue

        # visit
        visited.add(visiting)
        expanded = expanded + "," + visiting.seq

        # evaluate
        if visiting.seq == goal:
            print(visiting.path)
            print(expanded)
            return

        # insert children into fringe and recurse
        for child in visiting.children:
            fringe.put(child)

        i+=1
        
    print("No solution found.")
    print(expanded)



def DFS(fileName):
    start, goal, forbiddens = readFile(fileName)

    if start == goal:
        print (start)
        print (start)
        return

    root = getFirstLevelStates(start)
    fringe = deque()
    visited = set()
    visited.add(root)
    expanded = root.seq
    
    #append children in fringe to explore
    for child in reversed(root.children):
        fringe.appendleft(child)

    i = 1
    while i < 1000:

        if not fringe:
            break
        # get next node in fringe
        visiting = fringe.popleft()
        visiting.generateChildren()

        # check for end branch condition (cycle occurance by unorignal node or forbidden.)
        if visiting in visited or visiting.seq in forbiddens:
            continue

        # visit 
        visited.add(visiting)
        expanded = expanded + "," + visiting.seq

        # evaluate
        if visiting.seq == goal:
            print(visiting.path)
            print(expanded)
            return

        # insert most recent child additions to front of fringe list.
        for child in reversed(visiting.children):
            fringe.appendleft(child)
                
        i+=1

    print("No solution found.")
    print(expanded)


def IDS(fileName):
    start, goal, forbiddens = readFile(fileName)

    if start == goal:
        print (start)
        print (start)
        return
    
    root = getFirstLevelStates(start)

    fringe = deque()
    visited = set()
    visited.add(root)
    expanded = root.seq

    # create fringe from root's children
    for child in reversed(root.children):
        fringe.appendleft(child)

    depthLimit = 0
    i = 1
    while i < 1000:

        # search finished with no results. increase depth limit by 1 and restart
        if not fringe:
            #clear variables
            visited.clear()
            # reset variables
            depthLimit+=1 
            visited.add(root)
            for child in reversed(root.children):
                fringe.appendleft(child)
            # append root to expanded again 
            expanded = expanded + "," + root.seq
            i+=1
            continue

        visiting = fringe.popleft()

        if visiting.depth == depthLimit and not visiting.seq in forbiddens:
            visiting.generateChildren() 

        # test for end branch conditions. (cycle occurance, forbidden, or at depth limit)
        if visiting in visited or visiting.seq in forbiddens or visiting.depth > depthLimit:
            continue

        # visit 
        visited.add(visiting)
        expanded = expanded + "," + visiting.seq

        # evaluate
        if visiting.seq == goal:
            print(visiting.path)
            print(expanded)
            return

        # insert most recent child additions to front of fringe list.
        for child in reversed(visiting.children):
            fringe.appendleft(child)

        i+=1

    print("No solution found.")
    print(expanded)


def Greedy(fileName):
    start, goal, forbiddens = readFile(fileName)

    if start == goal:
        print (start)
        print (start)
        return

    root = getFirstLevelStates(start)
    count = 0
    fringe = queue.PriorityQueue()
    visited = set()
    visited.add(root)
    expanded = root.seq

    for child in root.children:
        count+=1
        # tuple (heuristic, expansion order for tie breaking, attached node)
        hWrap = dataclasses.astuple( nodeHwrap(h(goal, child.seq), -count, child) )
        fringe.put(hWrap) 

    i = 1
    while i < 1000:

        if fringe.empty():
            break

        # get next node in fringe
        nodeWrap = fringe.get()
        visiting = nodeWrap[2]

        visiting.generateChildren()
        
        if visiting in visited or visiting.seq in forbiddens:
            continue

        # visit
        visited.add(visiting)
        expanded = expanded + "," + visiting.seq
        
        # evaluate
        if visiting.seq == goal:
            print(visiting.path)
            print(expanded)
            return

        # add children to fringe with heuristic and order identifier 
        for child in visiting.children:
            count+=1
            # tuple (heuristic, expansion order for tie breaking, attached node)
            hWrap = dataclasses.astuple( nodeHwrap(h(goal, child.seq), -count, child) )
            fringe.put(hWrap) 

        i+=1

    print("No solution found.")
    print(expanded)


def Astar(fileName):
    start, goal, forbiddens = readFile(fileName)

    if start == goal:
        print (start)
        print (start)
        return

    root = getFirstLevelStates(start)
    count = 0
    fringe = queue.PriorityQueue()
    visited = set()
    visited.add(root)
    expanded = root.seq

    for child in root.children:
        count+=1
        # tuple (heuristic, expansion order for tie breaking, attached node)
        hWrap = dataclasses.astuple( nodeHwrap(h(goal, child.seq) + child.depth, -count, child) )
        fringe.put(hWrap) 

    i = 1
    while i < 1000:

        if fringe.empty():
            break

        # expand and visit child
        nodeWrap = fringe.get()
        visiting = nodeWrap[2]

        visiting.generateChildren()

        if visiting in visited or visiting.seq in forbiddens:
            continue

        # visit
        visited.add(visiting)
        expanded = expanded + "," + visiting.seq

        # evaluate
        if visiting.seq == goal:
            print(visiting.path)
            print(expanded)
            return

        # add children to fringe with heuristic and order identifier 
        for child in visiting.children:
            count+=1
            # tuple (heuristic, expansion order for tie breaking, attached node)
            hWrap = dataclasses.astuple( nodeHwrap(h(goal, child.seq) + child.depth, -count, child) )
            fringe.put(hWrap) 

        i+=1        

    print("No solution found.")
    print(expanded)


def HillClimb(fileName):
    start, goal, forbiddens = readFile(fileName)

    if start == goal:
        print (start)
        print (start)
        return

    root = getFirstLevelStates(start)
    count = 0
    fringe = queue.PriorityQueue()
    visited = set()
    visited.add(root)
    expanded = root.seq
    h_best = h(goal, root.seq)

    for child in root.children:
        count+=1
        # tuple (heuristic, expansion order for tie breaking, attached node)
        hWrap = dataclasses.astuple( nodeHwrap(h(goal, child.seq), -count, child) )
        fringe.put(hWrap) 

    i = 1
    while i < 1000:

        if fringe.empty():
            break

        # get next node in fringe
        nodeWrap = fringe.get()
        visiting = nodeWrap[2]
        h_visiting = nodeWrap[0]

        visiting.generateChildren()

        # check for originality and conditions
        if visiting in visited or visiting.seq in forbiddens or h_visiting >= h_best :
            continue

        # visit
        h_best = h_visiting
        visited.add(visiting)
        expanded = expanded + "," + visiting.seq
        
        # evaluate
        if visiting.seq == goal:
            print(visiting.path)
            print(expanded)
            return

        # remove all unselected nodes from fringe
        while not fringe.empty():
            fringe.get()

        # add children to fringe with heuristic and order identifier 
        for child in visiting.children:
            count+=1
            # tuple (heuristic, expansion order for tie breaking, attached node)
            hWrap = dataclasses.astuple( nodeHwrap(h(goal, child.seq), -count, child) )
            fringe.put(hWrap) 
                
        i+=1

    print("No solution found.")
    print(expanded)

##### Helper functions ##########

def readFile(fileName):
    fileIn = open(fileName, "r")
    lines = fileIn.readlines()
    fileIn.close()
    startState = lines[0].strip("\n")
    goalState = lines[1].strip("\n")
    if len(lines) == 2:
        forbiddens = []
    else:
        forbiddenStates = lines[2].strip("\n")
        forbiddens = forbiddenStates.split(",")

    return startState, goalState, forbiddens

def getFirstLevelStates(start):

    root = node(start)

    # Generate first 6 children noting postion changed
    # left
    if int(start[0]) != 0:
        seq = str(int(start[0])-1) + start[1:]
        child = node(seq, "L", root)
        root.addChild(child)
    if int(start[0]) != 9:
        seq = str(int(start[0])+1) + start[1:]
        child = node(seq, "L", root)
        root.addChild(child)
    # mid
    if int(start[1]) != 0:
        seq = start[0] + str(int(start[1])-1) + start[2]
        child = node(seq, "M", root)
        root.addChild(child)
    if int(start[1]) != 9:
        seq = start[0] + str(int(start[1])+1) + start[2]
        child = node(seq, "M", root)
        root.addChild(child)
    # right
    if int(start[2]) != 0:
        seq = start[:2] + str(int(start[2])-1)
        child = node(seq, "R", root)
        root.addChild(child)
    if int(start[2]) != 9:
        seq = start[:2] + str(int(start[2])+1)
        child = node(seq, "R", root)
        root.addChild(child)

    return root


def h(goal, node):
    s1 = abs(int(goal[0]) - int(node[0]))
    s2 = abs(int(goal[1]) - int(node[1]))
    s3 = abs(int(goal[2]) - int(node[2]))

    return s1 + s2 + s3


def main():
    searchType = str(sys.argv[1])
    fileName = str(sys.argv[2])

    if searchType == "B":
        BFS(fileName)

    if searchType == "D":
        DFS(fileName)

    if searchType == "I":
        IDS(fileName)

    if searchType == "G":
        Greedy(fileName)

    if searchType == "A":
        Astar(fileName)

    if searchType == "H":
        HillClimb(fileName)

main()
