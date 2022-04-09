import pygame 
import globals
globals.initialize()

def Index(x,y):
    if(x < 0 or y < 0 or x > globals.grid_w-1 or y > globals.grid_h -1):
        return -1
    return x + y * globals.grid_w

def dfs(cells, cell):
    cell.searched = True

    if cell.x == globals.finish_x  and cell.y == globals.finish_y:
        cell.path = True
        return cell
    
    top = cells[Index(cell.x, cell.y-1)]
    #if there is no line on top and not visited yet
    if cell.top == False and top.searched == False:
        found = dfs(cells, top) 
        if found != None:
            cell.path = True
            return found

    right = cells[Index(cell.x+1, cell.y)]
    if cell.right == False and right.searched == False:
        found = dfs(cells, right) 
        if found != None:
            cell.path = True
            return found

    bottom = cells[Index(cell.x, cell.y+1)]
    if cell.bottom == False and bottom.searched == False:
        found = dfs(cells, bottom) 
        if found != None:
            cell.path = True
            return found

    left = cells[Index(cell.x-1, cell.y)]
    if cell.left == False and left.searched == False:
        found = dfs(cells, left) 
        if found != None:
            cell.path = True
            return found
    
    return None