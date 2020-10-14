import random
import copy
import time

def conflict(row1, col1, row2, col2):
    return (col1 == col2 or  # same column
            row1 - col1 == row2 - col2 or  # same \ diagonal
            row1 + col1 == row2 + col2)  # same / diagonal


def fitness(board):
    # each column has exactly one queen // hence inter-column attacks do not occur ....
    # calculating the row attacks .....
    num_conflicts = 0
    for (r1, c1) in enumerate(board):
        for (r2, c2) in enumerate(board):
            if (r1, c1) != (r2, c2):
                num_conflicts += conflict(r1, c1, r2, c2)
    return num_conflicts


def make_random_population(k=100): # generating k random states....
    population = []
    for i in range(k):
        node=[]
        node = random.sample(range(0,8),8)
        population.append(node)
        # print(node)
    return population

def reproduce(x,y): # generating a child node by CROSS-OVER from parent nodes...
    k = random.randint(0,8)
    childnode = x[:k] + y[k:] 
    return childnode
 

def mutate(board): # With some random probabilty mutating some of the child..
    k = random.randint(0,7)
    mutated_child = copy.deepcopy(board)
    mutated_child[k] = random.randint(0,7)
    return mutated_child


def genetic_algorithm(k):
    count = 0
    population = make_random_population(k)
    while True:
        count+=1
        # if count %100 == 0:
        #     print("Iterations",count,"| Best State",population[0],"| Attacking Pairs",fitness(population[0]))
        if count > 100000:
            break
        if fitness(population[0])==0:
            print("\nFound a gobal optimal solution ",population[0],"Iterations Elapsed :" ,count)
            break
        new_population = []
        for i in range(0,len(population),2):
            x = population[i]
            if i+1 < len(population):
                y = population[i+1]
            else:
                continue
            child_1 = reproduce(x,y)
            if random.random() < 0.6:
                child_1 = mutate(child_1)
            child_2 = reproduce(y,x)
            if random.random() < 0.5:
                child_2 = mutate(child_2)
            new_population.append(child_1)
            new_population.append(child_2)
        new_population.sort(key = lambda x: fitness(tuple(x)))
        population = new_population
    if count > 100000:
        return False
    else:
        return True
        
for i in range(1,10):
    print("k = ",i*100)
    start = time.time()
    genetic_algorithm(i*100)
    end = time.time()
    print("Time Elapsed :{} seconds".format(end-start))
'''Output :
k =  100

Found a gobal optimal solution  [3, 6, 4, 1, 5, 0, 2, 7] Iterations Elapsed : 295
Time Elapsed :1.5827062129974365 seconds
k =  200

Found a gobal optimal solution  [3, 1, 6, 2, 5, 7, 0, 4] Iterations Elapsed : 624
Time Elapsed :6.388580560684204 seconds
k =  300

Found a gobal optimal solution  [5, 2, 0, 6, 4, 7, 1, 3] Iterations Elapsed : 2
Time Elapsed :0.0338590145111084 seconds
k =  400

Found a gobal optimal solution  [5, 3, 1, 7, 4, 6, 0, 2] Iterations Elapsed : 640
Time Elapsed :14.568952560424805 seconds
k =  500

Found a gobal optimal solution  [3, 6, 0, 7, 4, 1, 5, 2] Iterations Elapsed : 71
Time Elapsed :1.9144110679626465 seconds
k =  600

Found a gobal optimal solution  [5, 2, 6, 1, 3, 7, 0, 4] Iterations Elapsed : 2
Time Elapsed :0.05275607109069824 seconds
k =  700

Found a gobal optimal solution  [3, 0, 4, 7, 1, 6, 2, 5] Iterations Elapsed : 2
Time Elapsed :0.06690716743469238 seconds
k =  800

Found a gobal optimal solution  [1, 6, 4, 7, 0, 3, 5, 2] Iterations Elapsed : 179
Time Elapsed :7.355249404907227 seconds
k =  900

Found a gobal optimal solution  [3, 6, 4, 1, 5, 0, 2, 7] Iterations Elapsed : 2
Time Elapsed :0.07262158393859863 seconds '''






