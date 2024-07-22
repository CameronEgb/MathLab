from itertools import combinations
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

unlocked = True

def genPointsInZ(values, startingVal, endingVal, removePointsWithCoordinateMultiples):
    indicies = []
    for i in range(0, len(values)):
        if values[i] == 0:
            indicies.append(i)
            
    points = []
    for i in range(startingVal, endingVal):
        for j in range(startingVal, endingVal):
            if i==1 or j==1 or not removePointsWithCoordinateMultiples or (i % j != 0 and j % i != 0):
                for k in range(startingVal, endingVal):
                    if k==1 or i==1 or j==1 or not removePointsWithCoordinateMultiples or (i % k != 0 and k % i != 0 and j % k != 0 and k % i != 0):
                        point = values.copy()
                        point[indicies[0]] = i
                        point[indicies[1]] = j
                        point[indicies[2]] = k
                        point[len(values)-1] = 0 # hardcoded for n=4 multipath
                        print(point)
                        points.append(point)
    
    return points, indicies

def determinate(weights):
    """
    sum = 0
    size = len(weights)
    for i in range(0, size):
        prod = 1
        for j in range(0, size):
            if i != j:
                prod *= weights[j]
        sum += prod
    return sum
    """
    #multipath det
    prod = 1
    for i in range(0, len(weights)-1):
        prod *= weights[i]
        
    return prod 

def generate_A(weights, columnNumber):
    totalSum = 0
    
    size = len(weights)
    A = [[0 for i in range(size)] for j in range(size)]
    
    #for each index in A
    for i in range(1, size):
        for j in range(i, size):
            #print(str(i) + " :   i,j   : " + str(j))

            """
            #Computation for number of 2-component forests such that
            #one component contains v1, and the other contains v_i and v_j
            for a in range(0, i):
                for b in range(j, size):
                    #print(str(a) + " : a,b : " + str(b))

                    prod = 1
                    for k in range(0, size):
                        if k != a and k != b:
                            prod *= weights[k]
                    A[i][j] += prod
                    if i != j:
                        A[j][i] += prod
            """
            
            # Recalculation for multipath         
            for a in range(0, i):
                prod = 1
                for b in range(0, size):
                    if b != a:
                        prod *= weights[b]
                A[i][j] += prod
                if i != j:
                        A[j][i] += prod
                
    #print(A)
    return A

def generate_mA(det, A, m):
    mA = [0]
    for i in range(0, m):
        for a in range(0, len(mA)):
            for b in range(0, len(A)):
                mA.append((mA[a]+ A[b]) % det)
    return list(set(mA))

numberOfConditions = 5
def getCondID(nums):
    if(nums[0] == nums[1]):
        return 1
    elif(nums[1] == nums[2]):
        return 2
    elif(nums[2] == nums[0] or nums[2] == 1):
        return 3
    elif(2*nums[0] == nums[2] or nums[0] == 2*nums[2]):
        return 4
    else:
        return 0
    








def computeExistance(jIndex, m, start, end, graph, printing, removeNonRelativelyPrimePoints):
        
    print('Graph Weights  ---  Laplacian Generalized Inverse Column ' +str(jIndex)+ '  ---  Satisfying x_0(s)');
    existance = [[[], [], []] for _ in range(0, numberOfConditions)] 
    nonExistance = [[[], [], []] for _ in range(0, numberOfConditions)] 
    points, indicies = genPointsInZ(graph, start, end, removeNonRelativelyPrimePoints)
    for weights in points:
        
        det = determinate(weights)
        A = generate_A(weights, m)[jIndex]
        mA = generate_mA(det, A, m)
        x0 = []
        for i in range(0, len(mA)):
            for j in range(0, len(A)):
                if (mA[i] - A[j] + det)%det not in mA:
                    break;
                if j == len(A)-1:
                    x0.append(mA[i])
                     
        #See if it fits any nice cases
        nums = []
        for i in range(0, 3):
            nums.append(weights[indicies[i]])
        cond = getCondID(nums)
        
        if len(x0) != 0: 
            for i in range(0, 3):
                existance[cond][i].append(nums[i])
        else:
            for i in range(0, 3):
                nonExistance[cond][i].append(nums[i])    
              
        if printing and x0 is not []:
            weights_str = "[" + ', '.join(f"{weight}" for weight in weights) + "]"
            A_str = "[" + ', '.join(f"{a}" for a in A) + "]"
            x0_str = "[" + ', '.join(f"{x}" for x in x0) + "]"
            print("{:<5} {:<18} {:<25} {:<20}".format(det, weights_str, A_str, x0_str));
       
    return existance, nonExistance


# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')




graph = [1, 0, 1, 0, 1, 0, 1, 1]
m = 1
plottingExistance = True
From = 1
To = 30
printing = True
removePointsWithCoordinateMultiples = True
#existance[Column of G.I][CoditionID][Coordinate Index]  
                 
#"""
existance = []
nonExistance = []
for j in [3]:
    existanceJ, nonExistanceJ = computeExistance(j, m, From, To, graph, printing, removePointsWithCoordinateMultiples)
    existance.append(existanceJ)
    nonExistance.append(nonExistanceJ)
# Plot the data points

if(plottingExistance):
    for i in range(0, numberOfConditions):
        #for j in [range(0, len(graph) - 1)]:
            #ax.scatter(existance[j][i][0], existance[j][i][1], existance[j][i][2], c='k', marker='x', label='None')
        ax.scatter(existance[0][i][0], existance[0][i][1], existance[0][i][2], c='k', marker='x', label='None')
                         ### switch to ***existance[j][i] or something
else:
    for i in range(0, numberOfConditions):
        #for j in [range(0, len(graph) - 1)]:
            #ax.scatter(existance[j][i][0], existance[j][i][1], existance[j][i][2], c='k', marker='x', label='None')
        ax.scatter(nonExistance[0][i][0], nonExistance[0][i][1], nonExistance[0][i][2], c='k', marker='x', label='None')
                         ### switch to ***existance[j][i] or something
#"""

 
# Show the plot
plt.show()