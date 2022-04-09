import globals
globals.initialize()

def Index(x,y):
    if(x < 0 or y < 0 or x > globals.grid_w-1 or y > globals.grid_h -1):
        return -1
    return x + y * globals.grid_w

def draw_path(v):
    v.path = True
    if v.parent != 0:
        draw_path(v.parent)

def myFunc(e):
  return e.distance

def dijkstra(cells, cell):
    queue = []
    cell.distance = 0
    # queue with inital cell
    queue.append(cell)

    # loop unitl queue not empty
    while len(queue) > 0:
        currentCell = queue.pop(0)  # next neighbor - closest
        currentCell.searched = True  # mark searched

        if currentCell.x == globals.finish_x and currentCell.y == globals.finish_y:
            draw_path(currentCell)
            globals.dijkstra_found_path = True
            break

        # get neighbors
        neighbors = []
        top_cell    = cells[Index(currentCell.x, currentCell.y-1)]
        right_cell  = cells[Index(currentCell.x+1, currentCell.y)]
        bottom_cell = cells[Index(currentCell.x, currentCell.y+1)]
        left_cell   = cells[Index(currentCell.x-1, currentCell.y)]
        indeks = 0

        tabliczka = []
        for i in range(4):
            tabliczka.append(0)
        # if there is no line on top and not visited yet
        if currentCell.left == False and left_cell.searched == False:
            neighbors.append(left_cell)
            tabliczka[0] = left_cell
            indeks += 1

        if currentCell.bottom == False and bottom_cell.searched == False:
            neighbors.append(bottom_cell)
            tabliczka[1] = bottom_cell
            indeks += 1

        if currentCell.right == False and right_cell.searched == False:
            neighbors.append(right_cell)
            tabliczka[2] = right_cell
            indeks += 1

        if currentCell.top == False and top_cell.searched == False:
            neighbors.append(top_cell)
            tabliczka[3] = top_cell
            indeks += 1

        # check every neighbor
        for neighbor in neighbors:
            #check min dist to neighbor and update
            #dist is 1 between us and neighbor
            for i in range(4):
                if tabliczka[i] == neighbor:
                    if i == 0:
                        temp = neighbor.waga_left
                    if i == 1:
                        temp = neighbor.waga_down
                    if i == 2:
                        temp = neighbor.waga_right
                    if i == 3:
                        temp = neighbor.waga_up
                    minDistance = min(neighbor.distance, currentCell.distance + 1)
            if minDistance != neighbor.distance:
                neighbor.distance = minDistance;  
                neighbor.parent = currentCell;     

                # sort queue after updating distance 
                if neighbor in queue:
                    print("change")
                    for el in queue:
                        if el == neighbor:
                            el.distance = neighbor.distance
                            print("change")
                    #neighbor.distance = minDistance
                    queue.sort(key=myFunc)

            # add neighbor for later search
            if not(neighbor in queue):
                queue.append(neighbor)
                queue.sort(key=myFunc)
