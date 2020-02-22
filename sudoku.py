import numpy as np 
import time 

grid = np.zeros((9,9), dtype='int')
while True:
    try:
        print("Введите значения")
        for i in range(9):
            stringrow = input("")
            for j,character in enumerate(stringrow):
                grid[i][j] = int(character)
    except:
        print("Ошибка формата данных")
        continue
    break

#Getting the set of numbers within a number's group------------------------------------
dx = np.array([0,1,2,0,1,2,0,1,2])
dy = np.array([0,0,0,1,1,1,2,2,2])
def getgroupset(grid,groupx,groupy):
    s = set()
    tlx = groupx * 3                                                    #The x coordinate of the top left square in group
    tly = groupy * 3                                                    #The y coordinate of the top left square in group
    for i in range(9):
        s.add(grid[tly+dy[i]][tlx+dx[i]])
    return s

#Function to check if a sudoku grid is solved------------------------------------------
def solving(grid):
    s = set()

    #Check rows
    
    for row in grid:
        s.clear()
        for value in row:
            s.add(value)
        if list(s) != [1,2,3,4,5,6,7,8,9]:
            return False
    #Check columns
    
    grid = grid.transpose()
    for column in grid:
        s.clear()
        for value in column:
            s.add(value)
        if list(s) != [1,2,3,4,5,6,7,8,9]:
            return False
    grid = grid.transpose()

    #Check groups (3x3 squares)
    
    for groupx in range(3):
        for groupy in range(3):
            s = getgroupset(grid, groupx, groupy)
            if list(s) != [1,2,3,4,5,6,7,8,9]:
                return False
    return True

#Recursive function to solve the grid--------------------------------------------------
counter =  -1
def solve(grid):
    if solving(grid):                                                     #Return if solved (base case)
        return True, grid

    global counter
    counter+= 1
    min_no = 10                                                         #The min number of possibilities
    fullset = set([1,2,3,4,5,6,7,8,9])                                  #Set of numbers in each row, column and group
    tgrid = grid.transpose()                                            #Transposed Grid
    for y, row in enumerate(grid):
        for x, value in enumerate(row):
            if value == 0:
                setx = set(row)
                sety = set(tgrid[x])
                setgroup = getgroupset(grid, int(x/3), int(y/3))
                possible = fullset - setx -sety - setgroup              #Set of possible values
                
                if len(possible) < min_no:
                    miny = y
                    minx = x
                    min_pos = possible
                    min_no = len(possible)
                    
    #print(min_pos)
    #print(minx, miny)                                             
    for possibility in min_pos:
        grid[miny][minx] = possibility
        solved, solved_grid = solve(np.copy(grid))                      #Important!! Ensure a copy of the array is passed into the recursive function
        if solved:
            return True, solved_grid
    return False, False
    
start = time.time()
solved, grid = solve(grid)
if solved:
    print("Решено")
    print("Затраченное время", str(time.time()-start) + 's')
    print("Количество изменений:", counter)
    print (grid)
else:
    print("Не могу :(")

input("Жми энтер что бы выйти\n")