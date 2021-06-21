from time import perf_counter as counter
from random import choice, randint
from collections import deque

from matplotlib import pyplot as plt
from imageio import get_writer
import numpy as np


class RecursiveBacktracking:
    # 1. Choose a starting point in the field.
    # 2. Randomly choose a wall at that point and carve a passage through to the adjacent cell, but only if the adjacent cell has not been visited yet. This becomes the new current cell.
    # 3. If all adjacent cells have been visited, back up to the last cell that has uncarved walls and repeat.
    # 4. The algorithm ends when the process has backed all the way up to the starting point.
    def __init__(self, mH, mW):
        self.mH      = mH
        self.mW      = mW
        self.GenTime = -1        
        self.maze    = np.zeros((2*self.mH+1, 2*self.mW+1), dtype=np.uint8)
        
        startH       = randint(0, self.mH - 1)
        startW       = randint(0, self.mW - 1)
        self.start   = (startH, startW)
        self.current = self.start
        self.visited = {self.current}
        self.stacked = deque(((self.current),))
    
    def isVisited(self, dstH, dstW):
        return (dstH, dstW) in self.visited
    
    def withinBorder(self, dstH, dstW):
        return (-1 < dstH < self.mH) and (-1 < dstW < self.mW)
    
    def possible(self, src):
        srcH, srcW = src
        cells      = []
        dHdW       = [[-1, 0], [ 1, 0], [ 0,-1], [ 0, 1]]
        
        for d, (dH, dW) in zip("udlr", dHdW):
            dstH, dstW = srcH + dH, srcW + dW
            if self.withinBorder(dstH, dstW) and not self.isVisited(dstH, dstW):
                cells.append((d, (dstH, dstW)))
        return cells
    
    def linkCells(self, d=None):        
        aH, aW = self.current   #array coordinates
        mH, mW = 2*aH+1, 2*aW+1 # maze coordinates
        
        if   d == "u": self.maze[mH-2:mH,mW] = 255
        elif d == "d": self.maze[mH:mH+2,mW] = 255
        elif d == "l": self.maze[mH,mW-2:mW] = 255
        elif d == "r": self.maze[mH,mW:mW+2] = 255
        else         : self.maze[   mH,  mW] = 255 
                
    def gen(self, gif=False, debug=False):
        step    = 0
        start   = counter()
        self.linkCells()
        if gif: writer = get_writer(f"maze_{self.mH}x{self.mW}.gif", mode='I', duration=0.01)

        while self.current != self.start or step == 0:
            directions = self.possible(self.current)
            if len(directions) != 0:
                d, goto = choice(directions)
                if debug: print(f"{d} <{self.current}> <{goto}>")
                self.linkCells(d)
                self.current    = goto
                self.visited.add(self.current)
                self.stacked.append(self.current)
            else:
                self.linkCells()
                goto            = self.stacked.pop()
                self.current    = goto
                

            step += 1
            if gif: writer.append_data(self.maze)
            
        stop            = counter()
        self.GenTime    = stop - start
        if gif: writer.close()
