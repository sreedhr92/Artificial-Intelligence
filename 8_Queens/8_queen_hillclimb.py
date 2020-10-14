import copy
import random


def shuffled(iterable):
    items = list(iterable)
    random.shuffle(items)
    return items

def argmin(iterable):
	return min(shuffled(iterable),key = lambda x: heuristic(x))

def conflict(row1, col1, row2, col2):
    return (col1 == col2 or  # same column
            row1 - col1 == row2 - col2 or  # same \ diagonal
            row1 + col1 == row2 + col2)  # same / diagonal

def heuristic(board):
    # each column has exactly one queen // hence inter-column attacks do not occur ....
    # calculating the row attacks .....
    num_conflicts = 0
    for (r1, c1) in enumerate(board):
        for (r2, c2) in enumerate(board):
            if (r1, c1) != (r2, c2):
                num_conflicts += conflict(r1, c1, r2, c2)
    return num_conflicts

def next_states(board):
	child_nodes = set()
	for i in range(len(board)):
		cur = board[i]
		for j in range(len(board)):
			node = []
			node = copy.deepcopy(list(board))
			if cur != j:
				node[i] = j
				child_nodes.add(tuple(node))
	return child_nodes


def hillclimbing(board):
	current = board
	while True:
		neighbours = next_states(current)
		best_neighbour = argmin(neighbours)
		print("current:",current,heuristic(current))
		print("best   :",best_neighbour,heuristic(best_neighbour))
		print()
		if heuristic(current) <= heuristic(best_neighbour):
			break
		current = best_neighbour
	print("Reached Local minima of the problem :",current)

board =(0,1,2,3,4,5,6,7)
hillclimbing(board)
'''
current: (3, 1, 5, 2, 8, 5, 3, 1) 10
best   : (3, 1, 4, 2, 8, 5, 3, 1) 6

current: (3, 1, 4, 2, 8, 5, 3, 1) 6
best   : (3, 6, 4, 2, 8, 5, 3, 1) 2

current: (3, 6, 4, 2, 8, 5, 3, 1) 2
best   : (3, 6, 4, 2, 8, 5, 7, 1) 0

current: (3, 6, 4, 2, 8, 5, 7, 1) 0
best   : (3, 6, 0, 2, 8, 5, 7, 1) 0

Reached Local minima of the problem : (3, 6, 4, 2, 8, 5, 7, 1) '''
