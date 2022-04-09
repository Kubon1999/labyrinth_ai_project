import globals, math

def Index(x,y):
    if(x < 0 or y < 0 or x > globals.grid_w-1 or y > globals.grid_h -1):
        return -1
    return x + y * globals.grid_w

def calc_dinstance_to_end(cells):
    for cell in cells:
        #h = abs(cell.x - globals.grid_w-1) + abs(cell.y - globals.grid_h-1) #Manhattan Distance
        h = math.sqrt( (cell.x - globals.finish_x )**2 + (cell.y - globals.finish_y )**2 ) #Euclidean Distance
        cell.distance_from_end = h

def distance_between(start,stop):
        return abs(start.x - stop.x) + abs(start.y - stop.y)

def draw_path(v):
    v.path = True
    if v.parent != 0:
        draw_path(v.parent)

def a_star(cells, cell):
    calc_dinstance_to_end(cells)
    closedset = []              #  cells that are visited already
    openset = []
    openset.append(cell) # cells unvisited but to visit in future
    g_score = []
    for _ in cells:
        g_score.append(0)
    g_score[Index(cell.x, cell.y)] = 0                        # length of optimal path
    h_score = []
    for _ in cells:
        h_score.append(0)
    f_score = []
    for _ in cells:
        f_score.append(0)
    while len(openset) > 0:
        currentCell = openset.pop(0) # cell ktory ma najmniejsze f_score[] value
        currentCell.searched = True 
        if currentCell.x == globals.finish_x  and currentCell.y == globals.finish_y :
            draw_path(currentCell)
            break
        closedset.append(currentCell)

        #find neighbors
        # get neighbors
        neighbors = []
        top_cell    = cells[Index(currentCell.x, currentCell.y-1)]
        right_cell  = cells[Index(currentCell.x+1, currentCell.y)]
        bottom_cell = cells[Index(currentCell.x, currentCell.y+1)]
        left_cell   = cells[Index(currentCell.x-1, currentCell.y)]

        # if there is no line on top and not visited yet
        if currentCell.left == False and left_cell.searched == False:
            neighbors.append(left_cell)

        if currentCell.bottom == False and bottom_cell.searched == False:
            neighbors.append(bottom_cell)

        if currentCell.right == False and right_cell.searched == False:
            neighbors.append(right_cell)

        if currentCell.top == False and top_cell.searched == False:
            neighbors.append(top_cell)

        for y in neighbors:
            if y in closedset:
                continue
            tentative_g_score = g_score[Index(currentCell.x, currentCell.y)] + distance_between(currentCell,y)
            tentative_is_better = False
            if y not in openset:
                openset.append(y)
                h_score[Index(y.x, y.y)] = y.distance_from_end
                tentative_is_better = True
            elif tentative_g_score < g_score[Index(y.x, y.y)]:
                tentative_is_better = True
            if tentative_is_better == True:
                y.parent = currentCell
                g_score[Index(y.x, y.y)] = tentative_g_score
                f_score[Index(y.x, y.y)] = g_score[Index(y.x, y.y)] + h_score[Index(y.x, y.y)] # estimated distance from start to end thru y
    return False