
# Maximum Capacity of each of th jugs
j1 = 8
j2 = 5
j3 = 3
explored = set()
path_global = []
frontier = []

# Each state is represented by 3 tuple....

def print_path(path):
	print(path)

# final_goal_state is a=4 or b=4
def next_state(s):
	a = s[0]
	b = s[1]
	c = s[2]
	path =[]
	#pouring A to other jugs...
	if a > 0:
	#pouring A to B....
		if a+b <= j2:
			path.append((0, a+b, c))
		else:
			a = a-(j2-b)
			path.append((a, j2, c))
		a = s[0]
		b = s[1]
		c = s[2]
	#pouring A to C....
		if a+c <= j3:
			path.append((0, b, a+c))
		else:
			a = a-(j3-c)
			path.append((a, b, j3))
	a = s[0]
	b = s[1]
	c = s[2]
	#pouring b to other jugs
	if b > 0:
		#pouring B to A..
		if b+a <= j1:
			path.append((a+b, 0, c))
		else:
			b = b-(j1-a)
			path.append((j1, b, c))
	#pouring B to C...
		a = s[0]
		b = s[1]
		c = s[2]
		if b+c <= j3:
			path.append((a, 0, b+c))
		else:
			b = b-(j3-c)
			path.append((a, b, j3))
	a = s[0]
	b = s[1]
	c = s[2]
	if c > 0:
	#pouring C to A..
		if a+c <= j1:
			path.append((a+c, b, 0))
		else:
			c = c - (j1-a)
			path.append((j1, b, c))
		a = s[0]
		b = s[1]
		c = s[2]
	#pouring C to B..
		if c+b <= j2:
			path.append((a, c+b, 0))
		else:
			c = c - (j2-b)
			path.append((a, j2, c))
	return path

# Using BFS to implement the searching process....
def bfs(s):
	flag = 0
	frontier.append(s)
	while len(frontier)!=0:
		state = frontier.pop(0)
		if state in explored:
			continue
		for i in next_state(state):
			if i in explored :
				continue
			if i[0] == 4 or i[1] == 4:
				print("Reached Goal State",i)
				path_global.append(i)
				flag=1
				break
			else:
				frontier.append(i)
		if flag == 1:
			break
		explored.add(state)
		path_global.append(state)

# initial State
initial = (8,0,0)
bfs(initial)
print("\nPath :")
print_path(path_global)
print("\nNo of nodes discovered ",len(explored))

'''Output:
Reached Goal State (1, 4, 3)

Path :
[(8, 0, 0), (3, 5, 0), (5, 0, 3), (0, 5, 3), (3, 2, 3), (5, 3, 0), (6, 2, 0), (2, 3, 3), (6, 0, 2), (2, 5, 1), (1, 4, 3)]

No of nodes discovered  10
'''