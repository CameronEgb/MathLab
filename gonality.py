from math import ceil
from itertools import combinations
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import sys
from itertools import product

orig_stdout = sys.stdout
f = open('out.txt', 'w')
#sys.stdout = f
#MIN from r to rn of k plus the sum from 1 to r-1 of (i)#((k/r-i+1) < l < (k/r-i)) plus r#(l>k)


def generate_arrays(n, y):
    return list(product(range(1, y), repeat=n))

def computeGonalities(Graph, maxComputedGonality):
    list(Graph).sort()
    GonalitySequence = []
    winningConfigurations = []
    for r in range (1, maxComputedGonality + 1): 
    #GonalitySequence = []
    
        #print("R-gon for r = " +str(r))
        minWinningDivisorChipCount = float('inf')
        winningConfig = []
        
        for maxMiddleChips in range (r, (len(Graph)+1) * r):
            #countArr = [maxMiddleChips]
            tail = r * sum(j > maxMiddleChips for j in Graph)
            winningDivisorChipCount = maxMiddleChips + tail
            
            if r < 3:
                for i in range(1, r):
                    #count = sum(j > maxMiddleChips*i/r for j in Graph) + sum (j <= (maxMiddleChips*(i+1))/r for j in Graph) - len(Graph)
                    #countArr.append(count)
                    #print("count = " + str(count) + " when i = " + str(i))
                    count = sum(j > maxMiddleChips/(r-i+1) for j in Graph) + sum (j <= (maxMiddleChips)/(r-i) for j in Graph) - len(Graph)
                    winningDivisorChipCount += (i) * count
            #countArr.append(tail)            
            
            if r == 2:
                maxLower = 0
                minUpper = float('inf')
                for l in Graph:
                    if l <= maxMiddleChips/2:
                        if l > maxLower:
                            maxLower = l
                    if l > maxMiddleChips/2:
                        if l < minUpper: 
                            minUpper = l
                if minUpper + maxLower <= maxMiddleChips:
                    winningDivisorChipCount -= 1
                
            if r == 3:
                j = 0
                for i in range(len(Graph)-2):
                    if Graph[i] + Graph[i+1] + Graph[i+2] > maxMiddleChips:
                        j = i + 2
                        break
                
                minToAdd = float('inf')
                for i in range(Graph[j]):
                    toAdd = sum(i < j <= maxMiddleChips - i for j in Graph) + 2 * sum(maxMiddleChips - i < j <= maxMiddleChips for j in Graph)
                    if toAdd < minToAdd:
                        minToAdd = toAdd
                #print(minToAdd)
                winningDivisorChipCount += minToAdd
            #print("Current Winning Divisor Chip Count: " +str(winningDivisorChipCount) + " Chips in middle: " +str(maxMiddleChips))
            if winningDivisorChipCount < minWinningDivisorChipCount:
                minWinningDivisorChipCount = winningDivisorChipCount
                #winningConfig = countArr
        
        GonalitySequence.append(minWinningDivisorChipCount)
        winningConfigurations.append(winningConfig)
    
    return winningConfigurations, GonalitySequence

def plotGraphs(n, y):
    Graphs = generate_arrays(n, y)
    Gonalities = [[], [], []]
    interestingGraphs = []
    for G in Graphs:
        winningConfigs, currnetGons = computeGonalities(G, 3)
        Gonalities[0].append(currnetGons[0])
        Gonalities[1].append(currnetGons[1])
        Gonalities[2].append(currnetGons[2])
        if (currnetGons[1] < (3/2) * currnetGons[0]):
            interestingGraphs.append(G)
            print("Graph: " +str(G)+ ", Gonalities:" + str(currnetGons))
        #print("Graph: " +str(G)+ ", Gonalities:" + str(currnetGons))

    # Create a 3D plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel('Gon-2')
    ax.set_ylabel('Gon-3')
    #ax.set_zlabel('Gon-3')

    ax.scatter(Gonalities[1], Gonalities[2], c='k', marker='x', label='None')

    plt.show()
    
def computeDifferences(n, y):
    
    Graphs = generate_arrays(n, y)
    
    for G in Graphs:
        winningConfigs, currnetGons = computeGonalities(G, 3)
        for i in range(y + 3):
            winningConfigsPrime, currnetGonsPrime = computeGonalities(G + (i,), 3)

            if currnetGonsPrime[0] == currnetGons[0] + 1 and currnetGonsPrime[1] == currnetGons[1] + 1:
                print("Adding " +str(i)+ " to " +str(G)+ " gives gonality sequences " +str(currnetGons)+ " and " +str(currnetGonsPrime))
    
    
    return True   



Graph = (1,1,1,1,2,2)
configs, gonSeq = computeGonalities(Graph, 3)
splitGraph = [[] for _ in range(len(configs))]
print("Graph + configs: " +str(configs)+ " Gonalities: " + str(gonSeq))

plotGraphs(6, 12)
#computeDifferences(5, 10)

sys.stdout = orig_stdout
f.close()