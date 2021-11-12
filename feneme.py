import random as rd
import numpy as np
import matplotlib.pyplot as pyplot
import time as t
from queue import PriorityQueue



#--- the only significant change is that you enter (item, value) with put and receive item with get ---#

class my_priority_queue(PriorityQueue):
    def __init__(self):
        PriorityQueue.__init__(self)
        self.counter = 0

    def put(self, item, priority):
        PriorityQueue.put(self, (priority, self.counter, item))
        self.counter += 1

    def get(self, *args, **kwargs):
        _, _, item = PriorityQueue.get(self, *args, **kwargs)
        return item

#--- numpy aplicattion to color the maze by using arrays ---#
    
palletes =  {"maze":  np.array([[1.0, 1.0, 1.0],     #---      0 = white (path)       ---#
                                [0.0, 0.0, 0.0],     #---      1 = black (wall)       ---#
                                [0.0, 1.0, 0.0],     #---      2 = green (init)       ---#
                                [1.0, 0.0, 0.0],     #---      3 = red (target)       ---#
                                [1.0, 1.0, 0.0]])}   #---  4 = yellow (winning path)  ---#
    
def create_image(boolean_array, palette_name):
    return palletes[palette_name][boolean_array.astype(int)]




#-------------------------------- Maze Generator using Randomized Prim's Algorithm --------------------------------#




#--- every point in the grid is a wall that can turn into a path ---#
        
class Wall:
    
    def __init__(self, x, y):
        self.is_visited = False
        self.position = [x, y]
        self.is_path = False
        self.neighbors = []
        self.weight = rd.randint(1,100)
        self.open_neighbors = 0
    
    #--- simple function that returns all neighbors of one position in grid ---#
    
    def gen_neighbors(self, x, y, grid):    
        lines = len(grid)
        columns = len(grid[0])
        
        #--- if it's on the border of the grid, we add two or three neighbors. Else, we add four neighbors ---#
        
        if x == lines - 1:
            self.neighbors.append(grid[x - 1][y]) #--- upper ---#
        elif x == 0:
            self.neighbors.append(grid[x + 1][y]) #--- lower ---#
        else:
            self.neighbors.append(grid[x - 1][y])
            self.neighbors.append(grid[x + 1][y])
            
        if y == columns - 1:
            self.neighbors.append(grid[x][y - 1]) #--- left  ---#
        elif y == 0:
            self.neighbors.append(grid[x][y + 1]) #--- right ---#
        else:
            self.neighbors.append(grid[x][y - 1])
            self.neighbors.append(grid[x][y + 1])      
    
    #--- count the number of paths neighbors ---#
    
    def count_open_neigh(self):
        
        for neigh in self.neighbors:
            if neigh.is_path:
                self.open_neighbors += 1
    
    #--- if it's a path, returns 0; if it's a wall, return 1 ---#
    
    def draw(self):
        if self.is_path:
            return 0
        else:
            return 1
            

def make_maze(x, y):

    wall_list = my_priority_queue()
    
    #--- using three matrix, it was easier to localize whe points that I needed during the code ---#
    
    grid = [[Wall(i, j) for j in range(y)] for i in range(x)]  #---  to get track of all objects   ---#
    matrix = [[j for j in range(y)] for i in range(x)]         #---         to be drawn            ---#
    matrix_weight = [[j for j in range(y)] for i in range(x)]  #--- matrix with all objects weight ---#
    
    for i in range(x):
        for j in range(y):
            matrix_weight[i][j] = grid[i][j].weight
    
    #--- generating all neighbors for all walls on grid ---#
    
    for i in range(x):
        for j in range(y):
            if i == 0 or i == x - 1 or j == 0 or j == y - 1: #--- if it's in the borders ---#
                grid[i][j].is_visited = True
            grid[i][j].gen_neighbors(i, j, grid)
    
    
    #--- using Randomized Prim's Algorithm to create Maze ---#
    
    first_cell = grid[1][1] #--- starting point ---#
    first_cell.is_path = True
    first_cell.is_visited = True
    
    for neigh in first_cell.neighbors:
        if not neigh.is_visited:
            wall_list.put(neigh, neigh.weight)
    
    while not wall_list.empty():
        cell = wall_list.get()
        cell.count_open_neigh()
        if cell.open_neighbors <= 1: #--- if it has less than 1 adjacent neighbor that is a path ---#
            cell.is_path = True
            cell.is_visited = True
            if cell.position[1] == 1 or cell.position[1] == y - 2: #--- exit must be on ther border and between maze's middle and bottom ---#
                if cell.position[0] > np.floor(x/2):
                    last_cell = cell #--- the last cell that is in the border to turn into a path is the target point in the maze ---#
            for neigh in cell.neighbors:
                if not neigh.is_visited:
                    if neigh.open_neighbors <= 1:
                        wall_list.put(neigh, neigh.weight)
        
    #--- drawing Maze as a matrix (0 - path; 1 - wall) ---#
    
    for i in range(x):
        for j in range(y):
            matrix[i][j] = grid[i][j].draw()
    
    matrix[1][0] = 2                                                   #--- entrance point = green ---#   
    if last_cell.position[1] == 1:                                     #---    exit point = red    ---#                                 
        matrix[last_cell.position[0]][last_cell.position[1] - 1] = 3
    else:
        matrix[last_cell.position[0]][last_cell.position[1] + 1] = 3
    
    #--- turning matrix into numpy array ---#
            
    maze = np.array([np.array(i) for i in matrix])
    print(maze)
    #--- printing the size of maze (without the borders) ---#
    
    print("                     Real Size:", x-2,"x",y-2)
    
    #--- ploting Maze ---#
    
    image = create_image(boolean_array=maze, palette_name='maze')
    pyplot.figure(figsize=(16, 8))
    pyplot.imshow(image, interpolation='nearest')
    pyplot.xticks([]), pyplot.yticks([])
    pyplot.show()
    
    return matrix, last_cell




#-------------------------------------- Path Finder using A* Search Algorithm --------------------------------------#




class Maze:
    
    def __init__(self, matrix, position, father):
        self.matrix = matrix
        self.position = position
        self.father = father
        self.neighbors = []
        self.distance = 0    

    #--- finding distance between current position in the maze and the exit ---#
    
    def find_distance(self, target):
        dX = abs(target[0] - self.position[0])
        dY = abs(target[1] - self.position[1])
        self.distance = dX + dY
    
    #--- generating all neighbors for the current position in the maze ---#
         
    def gen_neighbors(self, queue, maze_obj, target):
        if self.matrix[self.position[0] + 1][self.position[1]] == 0:
            enqueue_neighbor(queue, 
                             maze_obj, 
                             (self.position[0] + 1, self.position[1]),
                             target)
        if self.matrix[self.position[0] - 1][self.position[1]] == 0:
            enqueue_neighbor(queue, 
                             maze_obj, 
                             (self.position[0] - 1, self.position[1]),
                             target)
        if self.matrix[self.position[0]][self.position[1] + 1] == 0:
            enqueue_neighbor(queue, 
                             maze_obj, 
                             (self.position[0], self.position[1] + 1),
                             target)
        if self.matrix[self.position[0]][self.position[1] - 1] == 0:
            enqueue_neighbor(queue, 
                             maze_obj, 
                             (self.position[0], self.position[1] - 1),
                             target)

#--- unrolling all the path when it reaches the exit until it goes back to the start position ---#
            
def unroll(maze_obj):
    movements = []
    while maze_obj.father != 0:
        father = maze_obj.father
        movements.append(father.position)
        maze_obj = father
    return movements

#--- critical optimization that stops the code to look into a neighbors's maze if it's already a grandparent ---#

def is_grandparent(maze_obj, position):
        grandparent = maze_obj.father
        if grandparent != 0:
            if grandparent.position == position:
                return True
        return False
    
#--- used to put neighbors into the maze-tree and to make it possible to use the actual maze as a argument ---#

def enqueue_neighbor(queue, maze_obj, position, target):
    if not is_grandparent(maze_obj, position):
        neighbor_obj = Maze(maze_obj.matrix, position, maze_obj)
        neighbor_obj.find_distance(target)
        queue.put(neighbor_obj, neighbor_obj.distance)

#--- test if it's reached the exit ---#

def is_goal(maze, target):
    if maze.position[0] == target[0]:
        if maze.position[1] == target[1]:
            return True
    return False

#--- auxiliar solve function that calls all other functions and return the list of movements when the exit is reached ---#

def solve_aux(queue, target):
    maze_obj = queue.get()
    if is_goal(maze_obj, target):
        return unroll(maze_obj)
    else:
        maze_obj.gen_neighbors(queue, maze_obj, target)
        return solve_aux(queue, target)


#--- main function of this code ---#
    
    
def path_finder(x, y):
    start= t.time()
    
    #--- plotting the initial maze with the start as a green square and exit as a red square ---#
    
    print("                   #--- Initial Maze ---#")
    matrix, target = make_maze(x, y)
    
    #--- maze-tree is a priority queue that make it possible for us to use the A* search algorithm ---#
    
    maze_tree = my_priority_queue()
    
    
    target = target.position
    maze_obj = Maze(matrix, (1,1), 0)
    maze_obj.find_distance(target)
    maze_tree.put(maze_obj, maze_obj.distance)
    
    #--- list of movements to get to the exit of the maze ---#
    
    solution = solve_aux(maze_tree, target)[-1::-1]
    
    #--- changing the main matrix paths to another color if they are in the winning path ---#

    for i in solution:
        matrix[i[0]][i[1]] = 4
    matrix[1][0] = 4
    matrix[target[0]][target[1]] = 4
    if target[1] == 1:
        matrix[target[0]][target[1] - 1] = 4
    else:
        matrix[target[0]][target[1] + 1] = 4
    
    #--- turning matrix into numpy array ---#
            
    maze = np.array([np.array(i) for i in matrix])
    
    #--- printing final solution to the maze with the elapsed time ---#
    
    print("                   #--- Final Solution ---#")
    image = create_image(boolean_array=maze, palette_name='maze')
    pyplot.figure(figsize=(16, 8))
    pyplot.imshow(image, interpolation='nearest')
    pyplot.xticks([]), pyplot.yticks([])
    pyplot.show()
    print("             Elapsed Time: ", t.time() - start, "s")









    

make_maze(502,502)
