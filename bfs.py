import pygame, timeit
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

def bfs(cells, cell):
    queue = []
    queue.append(cell)
    #print(len(queue))
    while len(queue) > 0:
        v = queue.pop(0)
        if v.searched == False:
            v.searched = True
            if v.x == globals.finish_x  and v.y == globals.finish_y:
                draw_path(v)
                globals.bfs_found_path = True
                return True

            #check neighbouts and add those who are not visited yet
            top_cell = cells[Index(v.x, v.y-1)]
            #if there is no line on top and not visited yet
            if v.top == False and top_cell.searched == False:
                top_cell.parent = v
                queue.append(top_cell)
            
            right_cell = cells[Index(v.x+1, v.y)]
            if v.right == False and right_cell.searched == False:
                right_cell.parent = v
                queue.append(right_cell)

            bottom_cell = cells[Index(v.x, v.y+1)]
            if v.bottom == False and bottom_cell.searched == False:
                bottom_cell.parent = v
                queue.append(bottom_cell)

            left_cell = cells[Index(v.x-1, v.y)]
            if v.left == False and left_cell.searched == False:
                left_cell.parent = v
                queue.append(left_cell)