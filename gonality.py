from math import ceil
from itertools import combinations
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

#MIN from r to rn of k plus the sum from 1 to r-1 of (i)#((k/r-i+1) < l < (k/r-i)) plus r#(l>k)

def generateGraphs(maxWeights):
    Graphs = []
    for a in range(1, maxWeights):
        for b in range(1, maxWeights):
            for c in range(1, maxWeights):
                for d in range(1, maxWeights):
                    for e in range(1, maxWeights):
                        for f in range(1, maxWeights):
                            Graphs.append([a, b, c, d, e, f])

    return Graphs

def computeGonalities(Graph, maxComputedGonality):
    GonalitySequence = []
    winningConfigurations = []
    for r in range (1, maxComputedGonality + 1): 
    #GonalitySequence = []
    
        #print("R-gon for r = " +str(r))
        minWinningDivisorChipCount = float('inf')
        winningConfig = []
        for maxMiddleChips in range (r, (len(Graph)+1) * r):
            countArr = [maxMiddleChips]
            tail = r * sum(j > maxMiddleChips for j in Graph)
            winningDivisorChipCount = maxMiddleChips + tail
            for i in range(1, r):
                #count = sum(j > maxMiddleChips*i/r for j in Graph) + sum (j <= (maxMiddleChips*(i+1))/r for j in Graph) - len(Graph)
                count = sum(j > maxMiddleChips/(r-i+1) for j in Graph) + sum (j <= (maxMiddleChips)/(r-i) for j in Graph) - len(Graph)
                countArr.append(count)
                #print("count = " + str(count) + " when i = " + str(i))
                winningDivisorChipCount += (i) * count
            countArr.append(tail)
            
            #print("Current Winning Divisor Chip Count: " +str(winningDivisorChipCount) + " Chips in middle: " +str(maxMiddleChips))
            if winningDivisorChipCount < minWinningDivisorChipCount:
                minWinningDivisorChipCount = winningDivisorChipCount
                winningConfig = countArr
        
        GonalitySequence.append(minWinningDivisorChipCount)
        winningConfigurations.append(winningConfig)
    
    return winningConfigurations, GonalitySequence

def plotGraphs():
    Graphs = generateGraphs(8)
    Gonalities = [[], [], []]
    for G in Graphs:
        currnetGons = computeGonalities(G, 3)
        Gonalities[0].append(currnetGons[0])
        Gonalities[1].append(currnetGons[1])
        Gonalities[2].append(currnetGons[2])
        print("Graph: " +str(G)+ ", Gonalities:" + str(currnetGons))

    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel('Gon-2')
    ax.set_ylabel('Gon-3')
    #ax.set_zlabel('Gon-3')

    ax.scatter(Gonalities[1], Gonalities[2], c='k', marker='x', label='None')

    plt.show()
    
    
Graph = [9, 9, 9, 9, 9, 9, 5, 2, 2]
configs, gonSeq = computeGonalities(Graph, 3)
splitGraph = [[] for _ in range(len(configs))]
print("Graph + configs: " +str(configs)+ " Gonalities: " + str(gonSeq))